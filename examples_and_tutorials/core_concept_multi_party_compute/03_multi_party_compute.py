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
    CONFIG_PARTY_1,
    CONFIG_N_PARTIES
)

async def main(args = None):
    parser = argparse.ArgumentParser(
        description="Create a secret on the Nillion network with set read/retrieve permissions"
    )

    parser.add_argument(
        "--store_id_1",
        required=True,
        type=str,
        help="Store ID of the 1st secret",
    )

    parser.add_argument(
        "--party_ids_to_store_ids",
        required=True,
        nargs='+',
        type=str,
        help="List of partyid:storeid pairs of the secrets, with each pair separated by a space",
    )

    args = parser.parse_args(args)

    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")

    # 1st party computes on secrets
    seed = CONFIG_PARTY_1["seed"]
    client_1 = create_nillion_client(
        UserKey.from_seed(seed),
        NodeKey.from_seed(seed)
    )
    user_id_1 = client_1.user_id
    party_id_1 = client_1.party_id

    # Create payments config and set up Nillion wallet with a private key to pay for operations
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )

    program_id=f"{user_id_1}/{CONFIG_PROGRAM_NAME}"

    # Bind the parties in the computation to the client to set inputs and output parties
    compute_bindings = nillion.ProgramBindings(program_id)
    compute_bindings.add_input_party(CONFIG_PARTY_1["party_name"], party_id_1)
    compute_bindings.add_output_party(CONFIG_PARTY_1["party_name"], party_id_1)
    store_id_1 = args.store_id_1

    print(f"Computing using program {program_id}")
    print(f"Party 1 secret store_id: {store_id_1}")

    party_ids_to_store_ids = {}
    i=0
    for pair in args.party_ids_to_store_ids:
        party_id, store_id = pair.split(':')
        party_name = CONFIG_N_PARTIES[i]['party_name']
        compute_bindings.add_input_party(party_name, party_id)
        party_ids_to_store_ids[party_id] = store_id
        i=i+1

    compute_time_secrets = nillion.Secrets({})
    
    # Get cost quote, then pay for operation to compute
    receipt_compute = await pay(
        client_1,
        nillion.Operation.compute(program_id, compute_time_secrets),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    # Compute on the secret with all store ids. Note that there are no compute time secrets or public variables
    compute_id = await client_1.compute(
        cluster_id,
        compute_bindings,
        [store_id_1] + list(party_ids_to_store_ids.values()),
        compute_time_secrets,
        nillion.PublicVariables({}),
        receipt_compute,
    )

    # Print compute result
    print(f"The computation was sent to the network. compute_id: {compute_id}")
    while True:
        compute_event = await client_1.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            print(f"🖥️  The result is {compute_event.result.value}")
            return compute_event.result.value
    
if __name__ == "__main__":
    asyncio.run(main())
