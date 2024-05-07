import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
import pytest
import importlib

from dotenv import load_dotenv

from config import (
    CONFIG_PROGRAM_NAME,
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
        "--store_id_1",
        required=True,
        type=str,
        help="Store ID of the 1st secret",
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

    # 1st party computes on secrets
    client_1 = create_nillion_client(
        getUserKeyFromFile(CONFIG_PARTY_1["userkey_file"]), 
        getNodeKeyFromFile(CONFIG_PARTY_1["nodekey_alternate_file"]),
    )
    user_id_1 = client_1.user_id
    party_id_1 = client_1.party_id

    program_id=f"{user_id_1}/{CONFIG_PROGRAM_NAME}"


    # Bind the parties in the computation to the client to set inputs and output parties
    compute_bindings = nillion.ProgramBindings(program_id)
    compute_bindings.add_input_party(CONFIG_PARTY_1["party_name"], party_id_1)
    compute_bindings.add_output_party(CONFIG_PARTY_1["party_name"], party_id_1)
    store_id_1 = args.store_id_1

    print(f"Computing using program {program_id}")
    print(f"Party 1 secret store_id: {store_id_1}")

    party_ids_to_store_ids = {}
    i=0
    for pair in args.party_ids_to_store_ids:
        party_id, store_id = pair.split(':')
        party_name = CONFIG_N_PARTIES[i]['party_name']
        compute_bindings.add_input_party(party_name, party_id)
        party_ids_to_store_ids[party_id] = store_id
        i=i+1
    
    # Compute on the secret with all store ids. Note that there are no compute time secrets or public variables
    compute_id = await client_1.compute(
        cluster_id,
        compute_bindings,
        [store_id_1] + list(party_ids_to_store_ids.values()),
        nillion.Secrets({}),
        nillion.PublicVariables({}),
    )

    # Print compute result
    print(f"The computation was sent to the network. compute_id: {compute_id}")
    while True:
        compute_event = await client_1.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            print(f"🖥️  The result is {compute_event.result.value}")
            return compute_event.result.value
    
if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    result = await store_secret_party_1.main()
    args = ['--user_id_1', result[0], '--store_id_1', result[1]]
    result = await store_secret_party_n.main(args)
    store_ids = result[1].split(' ', 1)
    args = ['--store_id_1', result[0], '--party_ids_to_store_ids', store_ids[0], store_ids[1]]
    result = await main(args)
    assert result == {'my_output': 8}
