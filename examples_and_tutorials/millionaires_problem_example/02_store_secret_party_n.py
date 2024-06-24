import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
import pytest

from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from config import CONFIG_N_PARTIES

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from helpers.nillion_client_helper import (
    create_nillion_client,
    pay,
    create_payments_config,
)
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")

# Bob and Charlie store their salaries in the network
async def main(args=None):
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
        "--program_id",
        required=True,
        type=str,
        help="Program ID of the millionaires program",
    )

    args = parser.parse_args(args)

    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")

    # start a list of store ids to keep track of stored secrets
    store_ids = []
    party_ids = []

    for party_info in CONFIG_N_PARTIES:
        party_seed = party_info["party_name"] + "_seed"
        client_n = create_nillion_client(
            UserKey.from_seed(party_seed),
            NodeKey.from_seed(party_seed),
        )
        party_id_n = client_n.party_id
        user_id_n = client_n.user_id

        payments_config_n = create_payments_config(chain_id, grpc_endpoint)
        payments_client_n = LedgerClient(payments_config_n)
        payments_wallet_n = LocalWallet(
            PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
            prefix="nillion",
        )

        party_name = party_info["party_name"]
        secret_name = party_info["secret_name"]
        secret_value = party_info["secret_value"]

        # Create a secret for the current party
        stored_secret = nillion.Secrets(
            {secret_name: nillion.SecretInteger(secret_value)}
        )

        # Create permissions object with default permissions for the current user
        permissions = nillion.Permissions.default_for_user(user_id_n)

        # Give compute permissions to Alice so she can use the secret in the specific millionionaires program by program id
        compute_permissions = {
            args.user_id_1: {args.program_id},
        }
        permissions.add_compute_permissions(compute_permissions)
        print(
            f"\n👍 {party_name} gives compute permissions on their secret to Alice's user_id: {args.user_id_1}"
        )

        receipt_store = await pay(
            client_n,
            nillion.Operation.store_values(stored_secret),
            payments_wallet_n,
            payments_client_n,
            cluster_id,
        )
        # Store the permissioned secret
        store_id = await client_n.store_values(
            cluster_id, stored_secret, permissions, receipt_store
        )

        store_ids.append(store_id)
        party_ids.append(party_id_n)

        print(
            f"\n🎉 {party_name} stored {secret_name}: {secret_value} at store id: {store_id}"
        )

    party_ids_to_store_ids = " ".join(
        [f"{party_id}:{store_id}" for party_id, store_id in zip(party_ids, store_ids)]
    )

    print(
        "\n📋⬇️  Copy and run the following command to run multi party computation using the secrets"
    )
    print(
        f"\npython3 03_multi_party_compute.py --program_id {args.program_id} --party_ids_to_store_ids {party_ids_to_store_ids}"
    )
    return [args.program_id, party_ids_to_store_ids]


if __name__ == "__main__":
    asyncio.run(main())


@pytest.mark.asyncio
async def test_main():
    pass
