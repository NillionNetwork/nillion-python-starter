# Import necessary libraries and modules
import asyncio
import py_nillion_client as nillion
import os
import sys
import pytest
import numpy as np
import time
from dotenv import load_dotenv

# Add the parent directory to the system path to import modules from it
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import helper functions for creating nillion client and getting keys
from dot_product.network.helpers.nillion_client_helper import create_nillion_client
from dot_product.network.helpers.nillion_keypath_helper import (
    getUserKeyFromFile,
    getNodeKeyFromFile,
)
import nada_algebra.client as na_client

# Load environment variables from a .env file
load_dotenv()
from dot_product.config.parameters import DIM


# Decorator function to measure and log the execution time of asynchronous functions
def async_timer(file_path):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Log the execution time to a file
            with open(file_path, "a") as file:
                file.write(f"{DIM}: {elapsed_time:.6f},\n")
            return result

        return wrapper

    return decorator


# Asynchronous function to store a program on the nillion client
@async_timer("bench/store_program.json")
async def store_program(client, user_id, cluster_id, program_name, program_mir_path):
    action_id = await client.store_program(cluster_id, program_name, program_mir_path)
    program_id = f"{user_id}/{program_name}"
    print("Stored program. action_id:", action_id)
    print("Stored program_id:", program_id)
    return program_id


# Asynchronous function to store secrets on the nillion client
@async_timer("bench/store_secrets.json")
async def store_secrets(
    client, cluster_id, program_id, party_id, party_name, secret_array, prefix
):
    stored_secret = nillion.Secrets(na_client.array(secret_array, prefix))
    secret_bindings = nillion.ProgramBindings(program_id)
    secret_bindings.add_input_party(party_name, party_id)

    # Store the secret for the specified party
    store_id = await client.store_secrets(
        cluster_id, secret_bindings, stored_secret, None
    )
    return store_id


# Asynchronous function to perform computation on the nillion client
@async_timer("bench/compute.json")
async def compute(
    client, cluster_id, compute_bindings, store_ids, computation_time_secrets
):
    compute_id = await client.compute(
        cluster_id,
        compute_bindings,
        store_ids,
        computation_time_secrets,
        nillion.PublicVariables({}),
    )

    # Monitor and print the computation result
    print(f"The computation was sent to the network. compute_id: {compute_id}")
    while True:
        compute_event = await client.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            print(f"🖥️  The result is {compute_event.result.value}")
            return compute_event.result.value


# Main asynchronous function to coordinate the process
async def main():
    print(f"USING: {DIM}")
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    userkey = getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    nodekey = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_1"))
    client = create_nillion_client(userkey, nodekey)
    party_id = client.party_id
    user_id = client.user_id
    party_names = na_client.parties(3)
    program_name = "main"
    program_mir_path = f"./target/{program_name}.nada.bin"

    # Store the program
    program_id = await store_program(
        client, user_id, cluster_id, program_name, program_mir_path
    )

    # Create and store secrets for two parties
    A = np.ones([DIM])
    A_store_id = await store_secrets(
        client, cluster_id, program_id, party_id, party_names[0], A, "A"
    )

    B = np.ones([DIM])
    B_store_id = await store_secrets(
        client, cluster_id, program_id, party_id, party_names[1], B, "B"
    )

    # Set up the compute bindings for the parties
    compute_bindings = nillion.ProgramBindings(program_id)
    [
        compute_bindings.add_input_party(party_name, party_id)
        for party_name in party_names[:-1]
    ]
    compute_bindings.add_output_party(party_names[-1], party_id)

    print(f"Computing using program {program_id}")
    print(f"Use secret store_id: {A_store_id}, {B_store_id}")

    computation_time_secrets = nillion.Secrets({"my_int2": nillion.SecretInteger(10)})

    # Perform the computation and return the result
    result = await compute(
        client,
        cluster_id,
        compute_bindings,
        [A_store_id, B_store_id],
        computation_time_secrets,
    )
    return result


# Run the main function if the script is executed directly
if __name__ == "__main__":
    asyncio.run(main())