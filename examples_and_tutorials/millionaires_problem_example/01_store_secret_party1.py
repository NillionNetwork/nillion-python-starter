import asyncio
import py_nillion_client as nillion
import os
import sys
import pytest

from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from config import CONFIG_PARTY_1

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

# Alice stores the millionaires program in the network
async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    seed = "alice_seed"
    client_alice = create_nillion_client(
        UserKey.from_seed(seed),
        NodeKey.from_seed(seed),
    )

    millionaires_program_name = "millionaires"

    # Note: check out the code for the full millionaires program in the nada_programs folder
    program_mir_path = "../../nada_programs-compiled/millionaires.nada.bin"

    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )

    # Pay to store the program
    receipt_store_program = await pay(
        client_alice,
        nillion.Operation.store_program(),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # Store millionaires program in the network
    print(f"Storing program in the network: {millionaires_program_name}")
    program_id = await client_alice.store_program(
        cluster_id, millionaires_program_name, program_mir_path, receipt_store_program
    )

    # Set permissions for the client to compute on the program
    permissions = nillion.Permissions.default_for_user(client_alice.user_id)
    permissions.add_compute_permissions({client_alice.user_id: {program_id}})

    user_id_alice = client_alice.user_id
    program_id = f"{user_id_alice}/{millionaires_program_name}"

    print(f"Alice stores millionaires program at program_id: {program_id}")
    print(f"Alice tells Bob and Charlie her user_id and the millionaires program_id")

    print(
        "\n📋⬇️ Copy and run the following command to store Bob and Charlie's salaries in the network"
    )
    print(
        f"\npython3 02_store_secret_party_n.py --user_id_1 {user_id_alice} --program_id {program_id}"
    )
    return [user_id_alice, program_id]


if __name__ == "__main__":
    asyncio.run(main())


@pytest.mark.asyncio
async def test_main():
    pass
