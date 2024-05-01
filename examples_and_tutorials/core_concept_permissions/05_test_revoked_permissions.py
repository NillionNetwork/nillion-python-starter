import argparse
import asyncio
import os
import sys
import pytest
import importlib

from dotenv import load_dotenv

fetch_reader_userid = importlib.import_module("01_fetch_reader_userid")
store_permissioned_secret = importlib.import_module("02_store_permissioned_secret")
retrieve_secret = importlib.import_module("03_retrieve_secret")
revoke_read_permissions = importlib.import_module("04_revoke_read_permissions")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()

async def main(args = None):
    parser = argparse.ArgumentParser(
        description="Check that retrieval permissions on a Secret have been revoked"
    )
    parser.add_argument(
        "--store_id",
        required=True,
        type=str,
        help="Store ID from the writer client store operation",
    )
    args = parser.parse_args(args)

    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    userkey = getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    nodekey = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_5"))
    
    # Reader Nillion client
    reader = create_nillion_client(userkey, nodekey)
    reader_user_id = reader.user_id

    try:
        secret_name = "my_int1"
        await reader.retrieve_secret(cluster_id, args.store_id, secret_name)
        print(f"⛔ FAIL: {reader_user_id} user id with revoked permissions was allowed to access secret", file=sys.stderr)
    except Exception as e:
        if str(e) == "retrieving secret: the user is not authorized to access the secret":
            print(f"🦄 Success: After user permissions were revoked, {reader_user_id} was not allowed to access secret", file=sys.stderr)
        else:
            raise(e)

if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    result = await fetch_reader_userid.main()
    args = ['--retriever_user_id', result]
    result = await store_permissioned_secret.main(args)
    args = ['--store_id', result]
    result = await retrieve_secret.main(args)
    args = ['--store_id', result[0], '--revoked_user_id', result[1]]
    result = await revoke_read_permissions.main(args)
    args = ['--store_id', result]
    await main(args)
