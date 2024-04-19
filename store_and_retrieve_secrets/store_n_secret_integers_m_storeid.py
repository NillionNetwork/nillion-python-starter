import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
import pytest

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()

# Test the limit M total secrets (store ids) stored with N SecretIntegers in each
# `python3 store_n_secret_integers_m_storeid.py --number_store_ids 100 --number_secret_integers 100`

async def main(args = None):
    parser = argparse.ArgumentParser(
        description="Store n secret integers in the Nillion network"
    )
    parser.add_argument(
        "--number_store_ids",
        required=True,
        type=int,
        help="number secrets",
    )
    parser.add_argument(
        "--number_secret_integers",
        required=True,
        type=int,
        help="number of secret integers to store",
    )

    args = parser.parse_args(args)

    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    userkey = getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    nodekey = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_1"))
    client = create_nillion_client(userkey, nodekey)

    # Dictionary to hold multiple secrets
    secrets = {}

    for x in range(1, args.number_store_ids + 1):

        for i in range(1, args.number_secret_integers + 1):
            secret_name = f"secret_{i}"
            secret_value = i
            secrets[secret_name] = nillion.SecretInteger(secret_value)

        secret_integer = nillion.Secrets(secrets)

        # Store multiple SecretIntegers
        store_id = await client.store_secrets(
            cluster_id, None, secret_integer, None
        )

        print(f"The secrets are stored at the #{x} store_id: {store_id}")

        # Optionally retrieve secrets
        for secret_name in secrets:
            result_tuple = await client.retrieve_secret(cluster_id, store_id, secret_name)
            print(f"The secret name as a uuid is {result_tuple[0]}")
            print(f"The secret value is {result_tuple[1].value}")

if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    result = await main()
    assert result == 100
