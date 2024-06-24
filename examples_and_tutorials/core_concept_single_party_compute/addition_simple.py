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

# 1 Party running simple addition on 1 stored secret and 1 compute time secret
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
    program_name = "addition_simple"
    program_mir_path = f"../../programs-compiled/{program_name}.nada.bin"

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
        client,
        nillion.Operation.store_program(),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # Store program, passing in the receipt that shows proof of payment
    action_id = await client.store_program(
        cluster_id, program_name, program_mir_path, receipt_store_program
    )

    # Print details about stored program
    program_id = f"{user_id}/{program_name}"
    print("Stored program. action_id:", action_id)
    print("Stored program_id:", program_id)

    ##### STORE SECRETS
    print("-----STORE SECRETS")

    # Create a secret
    stored_secret = nillion.Secrets(
        {
            "my_int1": nillion.SecretInteger(500),
        }
    )

    # Create a permissions object to attach to the stored secret
    permissions = nillion.Permissions.default_for_user(client.user_id)
    permissions.add_compute_permissions({client.user_id: {program_id}})

    # Get cost quote, then pay for operation to store the secret
    receipt_store = await pay(
        client,
        nillion.Operation.store_values(stored_secret),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # Store a secret, passing in the receipt that shows proof of payment
    store_id = await client.store_values(
        cluster_id, stored_secret, permissions, receipt_store
    )

    ##### COMPUTE
    print("-----COMPUTE")

    # Bind the parties in the computation to the client to set input and output parties
    compute_bindings = nillion.ProgramBindings(program_id)
    compute_bindings.add_input_party(party_name, party_id)
    compute_bindings.add_output_party(party_name, party_id)

    # Create a computation time secret to use
    computation_time_secrets = nillion.Secrets({"my_int2": nillion.SecretInteger(10)})

    # Get cost quote, then pay for operation to compute
    receipt_compute = await pay(
        client,
        nillion.Operation.compute(program_id, computation_time_secrets),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # Compute, passing all params including the receipt that shows proof of payment
    uuid = await client.compute(
        cluster_id=cluster_id,
        bindings=compute_bindings,
        store_ids=[store_id],
        secrets=computation_time_secrets,
        receipt=receipt_compute,
        public_variables=nillion.PublicVariables({}),
    )
    print(f"Computing using program {program_id}")
    print(f"Use secret store_id: {store_id}")

    # Print compute result
    print(f"The computation was sent to the network. compute_id: {uuid}")
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
    assert result == {"my_output": 510}
