import importlib
import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
import pytest

from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from helpers.nillion_client_helper import (
    create_nillion_client,
    pay,
    create_payments_config,
)

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")


fetch_reader_userid = importlib.import_module("01_fetch_reader_userid")
store_permissioned_secret = importlib.import_module("02_store_permissioned_secret")
retrieve_secret = importlib.import_module("03_retrieve_secret")
revoke_read_permissions = importlib.import_module("04_revoke_read_permissions")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from helpers.nillion_client_helper import create_nillion_client

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")

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
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    seed_1 = "seed_1"
    userkey = UserKey.from_seed(seed_1)
    nodekey = NodeKey.from_seed(seed_1)
    
    # Reader Nillion client
    reader = create_nillion_client(userkey, nodekey)
    reader_user_id = reader.user_id

    # Create payments config and set up Nillion wallet with a private key to pay for operations
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )

    # Get cost quote, then pay for operation to retrieve the secret
    receipt_store = await pay(
        reader,
        nillion.Operation.retrieve_value(),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    try:
        secret_name = "my_int1"
        await reader.retrieve_value(cluster_id, args.store_id, secret_name, receipt_store)
        print(f"⛔ FAIL: {reader_user_id} user id with revoked permissions was allowed to access secret", file=sys.stderr)
    except Exception as e:
        if str(e) == "retrieving value: the user is not authorized to access the secret":
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
