import asyncio
import os
import sys
import py_nillion_client as nillion
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()

async def main():
    userkey = getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    nodekey = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_1"))
    
    # Reader Nillion client
    reader = create_nillion_client(userkey, nodekey)
    # Get the reader's user id
    reader_user_id = reader.user_id()

    print("ℹ️ Fetched the reader's USER ID:", reader_user_id)
    print("\n\nRun the following command to store a secret and give read/retrieve permissions to the READER USER ID")
    print(f"\n📋 python3 02-store-permissioned-secret.py --retriever_user_id {reader.user_id()}")


asyncio.run(main())
