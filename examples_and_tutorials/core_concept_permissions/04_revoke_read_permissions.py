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

async def main(args = None):
    parser = argparse.ArgumentParser(
        description="Revoke user read/retrieve permissions from a secret on the Nillion network"
    )
    parser.add_argument(
        "--store_id",
        required=True,
        type=str,
        help="Store ID from the writer client store operation",
    )
    parser.add_argument(
        "--revoked_user_id",
        required=True,
        type=str,
        help="User ID of the reader python client (derived from user key)",
    )
    args = parser.parse_args(args)

    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    seed_2 = "seed_2"
    userkey = UserKey.from_seed(seed_2)
    nodekey = NodeKey.from_seed(seed_2)

    # Writer Nillion client
    writer = create_nillion_client(userkey, nodekey)

    # Create payments config and set up Nillion wallet with a private key to pay for operations
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )

    # Create new permissions object to rewrite permissions (reader no longer has retrieve permission)
    new_permissions = nillion.Permissions.default_for_user(writer.user_id)
    result = (
        "allowed"
        if new_permissions.is_retrieve_allowed(args.revoked_user_id)
        else "not allowed"
    )
    if result != "not allowed":
        raise Exception("failed to create valid permissions object")
    
    # Get cost quote, then pay for operation to update permissions
    receipt_update_permissions = await pay(
        writer,
        nillion.Operation.update_permissions(),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # Update the permission
    print(f"ℹ️ Updating permissions for secret: {args.store_id}.")
    print(f"ℹ️ Reset permissions so that user id {args.revoked_user_id} is {result} to retrieve object.", file=sys.stderr)
    await writer.update_permissions( cluster_id, args.store_id , new_permissions, receipt_update_permissions)

    print("\n\nRun the following command to test that permissions have been properly revoked")
    print(f"\n📋  python3 05_test_revoked_permissions.py  --store_id {args.store_id}")
    return args.store_id

if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    pass
