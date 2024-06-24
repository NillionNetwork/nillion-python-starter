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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from helpers.nillion_client_helper import (
    create_nillion_client,
    pay,
    create_payments_config,
)

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")

from config import (
    CONFIG_PROGRAM_NAME,
    CONFIG_N_PARTIES
)

# N other parties store a secret
async def main(args = None):
    parser = argparse.ArgumentParser(
        description="Create a secret on the Nillion network with set read/retrieve permissions"
    )
    parser.add_argument(
        "--user_id_1",
        required=True,
        type=str,
        help="User ID of the user who will compute with the secret being stored",
    )
    parser.add_argument(
        "--store_id_1",
        required=True,
        type=str,
        help="Store ID of the 1st secret",
    )

    args = parser.parse_args(args)

    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    program_id=f"{args.user_id_1}/{CONFIG_PROGRAM_NAME}"
    
    # start a list of store ids to keep track of stored secrets
    store_ids = []
    party_ids = []

    for party_info in CONFIG_N_PARTIES:
        seed = party_info["seed"]
        client_n = create_nillion_client(
            UserKey.from_seed(seed),
            NodeKey.from_seed(seed)
        )
        party_id_n = client_n.party_id
        user_id_n = client_n.user_id
        party_name = party_info["party_name"]
        secret_name = party_info["secret_name"]
        secret_value = party_info["secret_value"]

        # Create payments config and set up Nillion wallet with a private key to pay for operations
        payments_config = create_payments_config(chain_id, grpc_endpoint)
        payments_client = LedgerClient(payments_config)
        payments_wallet = LocalWallet(
            PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
            prefix="nillion",
        )

        # Create a secret for the current party
        stored_secret = nillion.Secrets({
            secret_name: nillion.SecretInteger(secret_value)
        })

       # Get cost quote, then pay for operation to store the secret
        receipt_store = await pay(
            client_n,
            nillion.Operation.store_values(stored_secret),
            payments_wallet,
            payments_client,
            cluster_id,
        )

        # Create permissions object
        permissions = nillion.Permissions.default_for_user(user_id_n)

        # Give compute permissions to the first party
        print(program_id)
        compute_permissions = {
            args.user_id_1: {program_id},
        }
        permissions.add_compute_permissions(compute_permissions)

        # Store the permissioned secret
        store_id = await client_n.store_values(
            cluster_id, stored_secret, permissions, receipt_store
        )

        store_ids.append(store_id)
        party_ids.append(party_id_n)

        print(f"\n🎉N Party {party_name} stored {secret_name}: {secret_value} at store id: {store_id}")
        print(f"\n🎉Compute permission on the secret granted to user_id: {args.user_id_1}")
        
    party_ids_to_store_ids = ' '.join([f'{party_id}:{store_id}' for party_id, store_id in zip(party_ids, store_ids)])

    print("\n📋⬇️ Copy and run the following command to run multi party computation using the secrets")
    print(f"\npython3 03_multi_party_compute.py --store_id_1 {args.store_id_1} --party_ids_to_store_ids {party_ids_to_store_ids}")
    return [args.store_id_1, party_ids_to_store_ids]

if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    pass
