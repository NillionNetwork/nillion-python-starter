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

# simple addition
# 1 party
# 2 secrets

async def main():
    basic_addition_program_id = "3S4FxK5161GUwK8NthMMLQrJ7xCyxvtnShzhhMdG8VPP4VcYG1bY6jz1yQP3Mp3cfeP19tWmVPUMJsbtATLgmkWu/basic_addition"
    cluster_id = os.getenv("NILLION_CLUSTER_ID")

    # get user key
    userkey_path = os.getenv("NILLION_USERKEY_PATH_PARTY_1")
    userkey = nillion.UserKey.from_file(userkey_path)

    # create nillion client
    client = create_nillion_client(userkey)

    # get the party id
    party_id = client.party_id()

    # create the 1st secret and store it in the network
    secret_to_be_stored = nillion.SecretInteger(42)
    secret_to_be_stored_name = "my_int1"
    single_party_name = "Party1"
    stored_secret = nillion.Secrets({secret_to_be_stored_name: secret_to_be_stored})

    # add bindings to the secret to designate which party (party id and party name) is inputing the secret to a program (program id)
    secret_bindings = nillion.ProgramBindings(basic_addition_program_id)
    secret_bindings.add_input_party(single_party_name, party_id)
    
    # store the secret
    store_id = await client.store_secrets(
        cluster_id, secret_bindings, stored_secret, None
    )
    print(f"Stored secret {stored_secret}, store_id ={store_id}")

    # create the 2nd secret and input it at computation time
    secret_for_computation = nillion.SecretInteger(24)
    computation_time_secret = nillion.Secrets({"my_int2": secret_for_computation})

    # bind the parties in the computation to the client
    compute_bindings = nillion.ProgramBindings(basic_addition_program_id)
    compute_bindings.add_input_party(single_party_name, party_id)
    compute_bindings.add_output_party(single_party_name, party_id)

    print(f"Computing using program {basic_addition_program_id}")
    print(f"Stored secret: {store_id}")
    print(f"Provided secret: {computation_time_secret}")
    
    compute_id = await client.compute(
        cluster_id,
        compute_bindings,
        [store_id],
        computation_time_secret,
        nillion.PublicVariables({}),
    )

    print(f"Computation sent to the network, compute_id = {compute_id}")
    print("Waiting computation response")
    while True:
        event = await client.next_compute_event()
        if isinstance(event, nillion.ComputeFinishedEvent):
            print(
                f"Received computation result for {event.uuid}, value = {event.result.value}"
            )
            break

    print(f"Retrieving secret from the network")
    result = await client.retrieve_secret(cluster_id, store_id, "my_int1")
    print(f"Retrieved secret, value = {result[1].value}")


asyncio.run(main())
