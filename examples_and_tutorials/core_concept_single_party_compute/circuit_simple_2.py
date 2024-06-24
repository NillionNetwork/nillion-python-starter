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

# 1 Party running a simple circuit on 6 stored secrets and 3 compute time secrets
async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    seed = "my_seed"
    userkey = UserKey.from_seed((seed))
    nodekey = NodeKey.from_seed((seed))
    client = create_nillion_client(userkey, nodekey)
    party_id = client.party_id
    user_id = client.user_id
    party_name = "Party1"
    program_name = "circuit_simple_2"
    program_mir_path = f"../../programs-compiled/{program_name}.nada.bin"

    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )

    # Pay to store the program
    receipt_store_program = await pay(
        client,
        nillion.Operation.store_program(),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # store program
    action_id = await client.store_program(
        cluster_id, program_name, program_mir_path, receipt_store_program
    )

    program_id = f"{user_id}/{program_name}"
    print("Stored program. action_id:", action_id)
    print("Stored program_id:", program_id)

    # Set permissions for the client to compute on the program
    permissions = nillion.Permissions.default_for_user(client.user_id)
    permissions.add_compute_permissions({client.user_id: {program_id}})

    # Create a secret
    stored_secret = nillion.Secrets(
        {
            "A": nillion.SecretInteger(3),
            "B": nillion.SecretInteger(14),
            "C": nillion.SecretInteger(5),
            "D": nillion.SecretInteger(6),
            "E": nillion.SecretInteger(2),
            "F": nillion.SecretInteger(1),
        }
    )

    receipt_store = await pay(
        client,
        nillion.Operation.store_values(stored_secret),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # Store a secret
    store_id = await client.store_values(
        cluster_id, stored_secret, permissions, receipt_store
    )

    # Bind the parties in the computation to the client to set input and output parties
    compute_bindings = nillion.ProgramBindings(program_id)
    compute_bindings.add_input_party(party_name, party_id)
    compute_bindings.add_output_party(party_name, party_id)

    print(f"Computing using program {program_id}")
    print(f"Use secret store_id: {store_id}")

    computation_time_secrets = nillion.Secrets(
        {
            "G": nillion.SecretInteger(9),
            "H": nillion.SecretInteger(10),
            "I": nillion.SecretInteger(7),
        }
    )

    # Pay for the compute
    receipt_compute = await pay(
        client,
        nillion.Operation.compute(program_id, computation_time_secrets),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # Compute on the secrets
    compute_id = await client.compute(
        cluster_id,
        compute_bindings,
        [store_id],
        computation_time_secrets,
        nillion.PublicVariables({}),
        receipt_compute,
    )

    # Print compute result
    print(f"The computation was sent to the network. compute_id: {compute_id}")
    while True:
        compute_event = await client.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            print(f"🖥️  The result is {compute_event.result.value}")
            return compute_event.result.value


if __name__ == "__main__":
    asyncio.run(main())


@pytest.mark.asyncio
async def test_main():
    result = await main()
    assert result == {"my_output": 319}
