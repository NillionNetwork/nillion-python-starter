from pdb import set_trace as bp
import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
from dotenv import load_dotenv

from config import (
    CONFIG_PARTY_1,
    CONFIG_N_PARTIES
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()

parser = argparse.ArgumentParser(
    description="Create a secret on the Nillion network with set read/retrieve permissions"
)

parser.add_argument(
    "--program_id",
    required=True,
    type=str,
    help="Program ID of the millionaires program",
)

parser.add_argument(
    "--party_ids_to_store_ids",
    required=True,
    nargs='+',
    type=str,
    help="List of partyid:storeid pairs of the secrets, with each pair separated by a space",
)


args = parser.parse_args()


async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")

    # 1st party computes on secrets
    client_1 = create_nillion_client(
        getUserKeyFromFile(CONFIG_PARTY_1["userkey_file"]), 
        getNodeKeyFromFile(CONFIG_PARTY_1["nodekey_file"])
    )
    party_id_1 = client_1.party_id()


    # Bind the parties in the computation to the client to set inputs and output parties
    compute_bindings = nillion.ProgramBindings(args.program_id)
    compute_bindings.add_input_party(CONFIG_PARTY_1["party_name"], party_id_1)
    compute_bindings.add_output_party(CONFIG_PARTY_1["party_name"], party_id_1)

    print(f"Computing using program {args.program_id}")

    party_ids_to_store_ids = {}
    i=0
    for pair in args.party_ids_to_store_ids:
        party_id, store_id = pair.split(':')
        party_name = CONFIG_N_PARTIES[i]['party_name']
        compute_bindings.add_input_party(party_name, party_id)
        party_ids_to_store_ids[party_id] = store_id
        i=i+1

    # Alice provides her salary at compute time
    party_name_alice = CONFIG_PARTY_1["party_name"]
    secret_name_alice = CONFIG_PARTY_1["secret_name"]
    secret_value_alice = CONFIG_PARTY_1["secret_value"]
    compute_time_secrets = nillion.Secrets({
        secret_name_alice: nillion.SecretInteger(secret_value_alice)
    })

    print(f"\n🎉 {party_name_alice} provided {secret_name_alice}: {secret_value_alice} as a compute time secret")

    # Compute on the secret with all store ids. Note that there are no compute time secrets or public variables
    compute_id = await client_1.compute(
        cluster_id,
        compute_bindings,
        list(party_ids_to_store_ids.values()),
        compute_time_secrets,
        nillion.PublicVariables({}),
    )

    # Print compute result
    print(f"The computation was sent to the network. compute_id: {compute_id}")
    while True:
        compute_event = await client_1.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            print(f"🖥️  The output result is {compute_event.result.value}")
            my_parties = CONFIG_N_PARTIES
            my_parties.insert(0, CONFIG_PARTY_1)
            richest_party = my_parties[compute_event.result.value["largest_position"]]["party_name"]
            print(f"The richest friend is {richest_party}")
            break
    
asyncio.run(main())
