import asyncio
import os
import py_nillion_client as nillion
from dotenv import load_dotenv
from nillion_client_helper import create_nillion_client

load_dotenv()

async def main():
    reader_userkey_path = os.getenv("NILLION_READERKEY_PATH")
    reader_userkey = nillion.UserKey.from_file(reader_userkey_path)
    
    # Reader Nillion client
    reader = create_nillion_client(reader_userkey)
    # Get the reader's user id
    reader_user_id = reader.user_id()

    print("ℹ️ Fetched the reader's USER ID:", reader_user_id)
    print("\n\nRun the following command to store a secret and give read/retrieve permissions to the READER USER ID")
    print(f"\n📋 python3 02-store-permissioned-secret.py --retriever_user_id {reader.user_id()}")


asyncio.run(main())
