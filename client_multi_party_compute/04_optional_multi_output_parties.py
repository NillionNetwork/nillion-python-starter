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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()

async def main(args = None):
    for party_info in CONFIG_N_PARTIES:
        client_n = create_nillion_client(
            getUserKeyFromFile(party_info["userkey_file"]), 
            getNodeKeyFromFile(party_info["nodekey_file"])
        )

        compute_event = await client_n.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            print(f"🖥️  {party_info['party_name']} can see the result is {compute_event.result.value}")
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
