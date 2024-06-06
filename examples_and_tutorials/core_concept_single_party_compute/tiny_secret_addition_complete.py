import asyncio
import py_nillion_client as nillion
import os
import sys
import pytest

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
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()


# This python script stores the tiny_secret_addition_complete program in the network, store secrets, and compute
async def main():
    # 0. The bootstrap-local-environment.sh script put nillion-devnet config variables into the .env file
    # Get cluster_id, gprc endpoint, chain id, user_key,node_key from the .env file
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_GRPC")
    chain_id = os.getenv("NILLION_CHAIN_ID")
    userkey = getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    nodekey = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_1"))

    # ✅ 1. Initialize NillionClient against nillion-devnet
    # Create Nillion Client for user
    client = create_nillion_client(userkey, nodekey)

    # ✅ 2. Get the user id and party id from NillionClient
    party_id = client.party_id
    user_id = client.user_id

    # ✅ 3. Create a payments config, payments client and payments wallet then pay for and store a compiled Nada program in the network
    # Set the program name
    program_name = "tiny_secret_addition_complete"
    # Set the path to the compiled program
    program_mir_path = f"../../programs-compiled/{program_name}.nada.bin"
    # Store the program
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_WALLET_PRIVATE_KEY"))),
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

    # Create a variable for the program_id, which is the {user_id}/{program_name}
    program_id = f"{user_id}/{program_name}"
    print("Stored program. action_id:", action_id)
    print("Stored program_id:", program_id)

    # ✅ 4. Create the 1st secret with bindings to the program
    # Create a secret named "my_int1" with any value, ex: 500
    new_secret = nillion.Secrets(
        {
            "my_int1": nillion.SecretInteger(500),
        }
    )

    # Set the input party for the secret
    # The party name needs to match the party name that is storing "my_int1" in the program
    party_name = "Party1"

    # Set permissions for the client to compute on the program
    permissions = nillion.Permissions.default_for_user(client.user_id)
    permissions.add_compute_permissions({client.user_id: {program_id}})

    # ✅ 5. Pay for and store the secret in the network and print the returned store_id
    receipt_store = await pay(
        client,
        nillion.Operation.store_secrets(new_secret),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    # Store a secret
    store_id = await client.store_secrets(
        cluster_id, new_secret, permissions, receipt_store
    )
    print(f"Computing using program {program_id}")
    print(f"Use secret store_id: {store_id}")

    # ✅ 6. Create compute bindings to set input and output parties
    compute_bindings = nillion.ProgramBindings(program_id)
    compute_bindings.add_input_party(party_name, party_id)
    compute_bindings.add_output_party(party_name, party_id)

    # ✅ 7. Pay for and compute on the program with 1st secret from the network, and the 2nd secret, provided at compute time

    # Add my_int2, the 2nd secret at computation time
    computation_time_secrets = nillion.Secrets({"my_int2": nillion.SecretInteger(10)})

    # Pay for the compute
    receipt_compute = await pay(
        client,
        nillion.Operation.compute(program_id, computation_time_secrets),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # Compute on the secret
    compute_id = await client.compute(
        cluster_id,
        compute_bindings,
        [store_id],
        computation_time_secrets,
        nillion.PublicVariables({}),
        receipt_compute,
    )

    # ✅ 8. Print the computation result
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
    assert result == {"my_output": 510}
