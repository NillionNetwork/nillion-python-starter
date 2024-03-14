from pdb import set_trace as bp
import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.nillion_client_helper import create_nillion_client

load_dotenv()

# Store secrets then compute on secrets
async def main():

    # Get cluster_id and userkey_path from the .env file
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    userkey_path = os.getenv("NILLION_USERKEY_PATH_PARTY_1")

    # Read user key from file
    userkey = nillion.UserKey.from_file(userkey_path)

    # Create Nillion Client for user
    client = create_nillion_client(userkey)

    # Get the party id and user id
    party_id = client.party_id()
    user_id = client.user_id()

    # Set the program id
    program_id=f"{user_id}/tiny_secret_addition"

    # Set the party name to match the party name from the stored program
    party_name="Party1"

    # Create a secret
    stored_secret = nillion.Secrets({
        "my_int1": nillion.SecretInteger(500),
    })

    # Create secret bindings to tie a secret to a program and set the input party
    secret_bindings = nillion.ProgramBindings(program_id)
    secret_bindings.add_input_party(party_name, party_id)

    # Store a secret
    store_id = await client.store_secrets(
        cluster_id, secret_bindings, stored_secret, None
    )

    print(f"Computing using program {program_id}")
    print(f"Use secret store_id: {store_id}")

    # Bind the parties in the computation to the client to set input and output parties
    compute_bindings = nillion.ProgramBindings(program_id)
    compute_bindings.add_input_party(party_name, party_id)
    compute_bindings.add_output_party(party_name, party_id)

    # Add the second secret at computation time
    computation_time_secrets = nillion.Secrets({"my_int2": nillion.SecretInteger(10)})
    
    # Compute on the secret
    compute_id = await client.compute(
        cluster_id,
        compute_bindings,
        [store_id],
        computation_time_secrets,
        nillion.PublicVariables({}),
    )

    # Print compute result
    print(f"The computation was sent to the network. compute_id: {compute_id}")
    while True:
        compute_event = await client.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            print(f"🖥️  The result is {compute_event.result.value}")
            break
    



    

asyncio.run(main())
