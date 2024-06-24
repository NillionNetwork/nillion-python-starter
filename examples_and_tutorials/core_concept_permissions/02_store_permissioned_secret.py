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
        description="Create a secret on the Nillion network with set read/retrieve permissions"
    )
    parser.add_argument(
        "--retriever_user_id",
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
    writer_user_id = writer.user_id
    print(writer_user_id, args.retriever_user_id)

    # Create payments config and set up Nillion wallet with a private key to pay for operations
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )

    # Create secret
    secret_name_1 = "my_int1"
    secret_1 = nillion.SecretInteger(10)

    secret_name_2 = "my_int2"
    secret_2 = nillion.SecretInteger(32)
    secrets_object = nillion.Secrets({secret_name_1: secret_1, secret_name_2: secret_2})

    # Writer gives themself default core_concept_permissions
    permissions = nillion.Permissions.default_for_user(writer_user_id)
    # Writer gives the reader permission to read/retrieve secret
    permissions.add_retrieve_permissions(set([args.retriever_user_id, writer_user_id]))

    result = (
        "allowed"
        if permissions.is_retrieve_allowed(args.retriever_user_id)
        else "not allowed"
    )
    if result == "not allowed":
        raise Exception("failed to set core_concept_permissions")
    
    print(f"ℹ️ Permissions set: Reader {args.retriever_user_id} is {result} to retrieve the secret")

    # Get cost quote, then pay for operation to store the secret
    receipt_store = await pay(
        writer,
        nillion.Operation.store_values(secrets_object),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # Writer stores the permissioned secret, resulting in the secret's store id
    print(f"ℹ️  Storing permissioned secret: {secrets_object}")
    store_id = await writer.store_values(
        cluster_id, secrets_object, permissions, receipt_store
    )

    print("ℹ️ STORE ID:", store_id)
    print("\n\nRun the following command to retrieve the secret by store id as the reader")
    print(f"\n📋 python3 03_retrieve_secret.py --store_id {store_id} --secret_name {secret_name_1}")
    return store_id

if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    pass
