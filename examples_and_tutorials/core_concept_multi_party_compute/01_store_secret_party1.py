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
    CONFIG_PARTY_1
)

# The 1st Party stores a secret
async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    seed_party_1 = CONFIG_PARTY_1["seed"]
    client_1 = create_nillion_client(
        UserKey.from_seed(seed_party_1), NodeKey.from_seed(seed_party_1)
    )
    user_id_1 = client_1.user_id
    program_mir_path=f"../../programs-compiled/{CONFIG_PROGRAM_NAME}.nada.bin"

    # Create payments config and set up Nillion wallet with a private key to pay for operations
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )

    ##### STORE PROGRAM
    print("-----STORE PROGRAM")

    # Get cost quote, then pay for operation to store program
    receipt_store_program = await pay(
        client_1,
        nillion.Operation.store_program(),
        payments_wallet,
        payments_client,
        cluster_id,
    )    

    # 1st Party stores program
    action_id = await client_1.store_program(
        cluster_id, CONFIG_PROGRAM_NAME, program_mir_path, receipt_store_program
    )

    program_id=f"{user_id_1}/{CONFIG_PROGRAM_NAME}"
    print('Stored program. action_id:', action_id)
    print('Stored program_id:', program_id)

    # Create a permissions object to attach to the stored secret
    permissions = nillion.Permissions.default_for_user(client_1.user_id)
    permissions.add_compute_permissions({client_1.user_id: {program_id}})


    ##### STORE SECRETS
    print("-----STORE SECRETS")

    # 1st Party creates a secret
    stored_secret_1 = nillion.Secrets({
        key: nillion.SecretInteger(value)
        for key, value in CONFIG_PARTY_1["secrets"].items()
    })

    # Get cost quote, then pay for operation to store the secret
    receipt_store = await pay(
        client_1,
        nillion.Operation.store_values(stored_secret_1),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # 1st Party stores a secret
    store_id_1 = await client_1.store_values(
        cluster_id, stored_secret_1, permissions, receipt_store
    )
    secrets_string = ", ".join(f"{key}: {value}" for key, value in CONFIG_PARTY_1["secrets"].items())
    print(f"\n🎉1️⃣ Party {CONFIG_PARTY_1['party_name']} stored {secrets_string} at store id: {store_id_1}")
    print("\n📋⬇️ Copy and run the following command to store N other party secrets")
    print(f"\npython3 02_store_secret_party_n.py --user_id_1 {user_id_1} --store_id_1 {store_id_1}")
    return [user_id_1, store_id_1]

if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    pass