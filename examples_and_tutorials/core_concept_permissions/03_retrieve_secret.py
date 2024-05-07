import argparse
import asyncio
import os
import sys
import pytest

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()

async def main(args = None):
    parser = argparse.ArgumentParser(
        description="Use read permissions to retrieve a secret owned by another user on the Nillion network"
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
    nodekey = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_3"))

    # Reader Nillion client
    reader = create_nillion_client(userkey, nodekey)
    reader_user_id = reader.user_id

    secret_name = "my_int1"

    # Reader retrieves the named secret by store id
    print(f"Retrieving secret as reader: {reader_user_id}")
    result = await reader.retrieve_secret(cluster_id, args.store_id, secret_name)

    print(f"🦄 Retrieved {secret_name} secret, value = {result[1].value}", file=sys.stderr)
    print("\n\nRun the following command to revoke the reader's retrieve permissions to the secret")
    print(f"\n📋 python3 04_revoke_read_permissions.py --store_id {args.store_id} --revoked_user_id {reader_user_id}")
    return [args.store_id, reader_user_id]

if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    pass
