import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
import pytest
import importlib

from dotenv import load_dotenv

from config import (
    CONFIG_PARTY_1,
    CONFIG_N_PARTIES
)

store_secret_party_1 = importlib.import_module("01_store_secret_party1")
store_secret_party_n = importlib.import_module("02_store_secret_party_n")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()

async def main(args = None):
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


    args = parser.parse_args(args)

    cluster_id = os.getenv("NILLION_CLUSTER_ID")

    # Alice initializes a client
    client_alice = create_nillion_client(
        getUserKeyFromFile(CONFIG_PARTY_1["userkey_file"]), 
        getNodeKeyFromFile(CONFIG_PARTY_1["nodekey_alternate_file"])
    )
    party_id_alice = client_alice.party_id

    # Create computation bindings for millionaires program
    compute_bindings = nillion.ProgramBindings(args.program_id)

    # Add Alice as an input party
    compute_bindings.add_input_party(CONFIG_PARTY_1["party_name"], party_id_alice)

    # Add an output party (Alice). 
    # The output party reads the result of the blind computation
    compute_bindings.add_output_party(CONFIG_PARTY_1["party_name"], party_id_alice)

    print(f"Computing using program {args.program_id}")

    # Also add Bob and Charlie as input parties
    party_ids_to_store_ids = {}
    i=0
    for pair in args.party_ids_to_store_ids:
        party_id, store_id = pair.split(':')
        party_name = CONFIG_N_PARTIES[i]['party_name']
        compute_bindings.add_input_party(party_name, party_id)
        party_ids_to_store_ids[party_id] = store_id
        i=i+1

    # Add any computation time secrets
    # Alice provides her salary at compute time
    party_name_alice = CONFIG_PARTY_1["party_name"]
    secret_name_alice = CONFIG_PARTY_1["secret_name"]
    secret_value_alice = CONFIG_PARTY_1["secret_value"]
    compute_time_secrets = nillion.Secrets({
        secret_name_alice: nillion.SecretInteger(secret_value_alice)
    })

    print(f"\n🎉 {party_name_alice} provided {secret_name_alice}: {secret_value_alice} as a compute time secret")

    # Compute on the secret with all store ids. Note that there are no compute time secrets or public variables
    compute_id = await client_alice.compute(
        cluster_id,
        compute_bindings,
        list(party_ids_to_store_ids.values()), # Bob and Charlie's stored secrets
        compute_time_secrets, # Alice's computation time secret
        nillion.PublicVariables({}),
    )

    # Print compute result
    print(f"The computation was sent to the network. compute_id: {compute_id}")
    while True:
        compute_event = await client_alice.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            print(f"🖥️  The output result is {compute_event.result.value}")

            # The compute result is an index
            # Map it to the corresponding party name who should pay for lunch
            # ['Alice', 'Bob', 'Charlie']
            my_parties = CONFIG_N_PARTIES
            my_parties.insert(0, CONFIG_PARTY_1)
            richest_party = my_parties[compute_event.result.value["largest_position"]]["party_name"]
            print(f"The richest friend is {richest_party}")
            return richest_party
    
if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    result = await store_secret_party_1.main()
    args = ['--user_id_1', result[0], '--program_id', result[1]]
    result = await store_secret_party_n.main(args)
    store_ids = result[1].split(' ', 1)
    args = ['--program_id', result[0], '--party_ids_to_store_ids', store_ids[0], store_ids[1]]
    result = await main(args)
    assert result == 'Charlie'
