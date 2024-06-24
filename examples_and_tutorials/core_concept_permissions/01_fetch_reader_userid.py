import asyncio
import os
import sys
import pytest

from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from helpers.nillion_client_helper import create_nillion_client

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")

async def main():
    seed_1 = "seed_1"
    userkey = UserKey.from_seed((seed_1))
    nodekey = NodeKey.from_seed((seed_1))
    
    # Reader Nillion client
    reader = create_nillion_client(userkey, nodekey)
    # Get the reader's user id
    reader_user_id = reader.user_id

    print("ℹ️ Fetched the reader's USER ID:", reader_user_id)
    print("\n\nRun the following command to store a secret and give read/retrieve permissions to the READER USER ID")
    print(f"\n📋 python3 02_store_permissioned_secret.py --retriever_user_id {reader_user_id}")
    return reader_user_id

if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    pass
