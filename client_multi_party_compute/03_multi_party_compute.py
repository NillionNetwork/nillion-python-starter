from pdb import set_trace as bp
import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
from dotenv import load_dotenv

from config import (
    CONFIG_PROGRAM_ID,
    CONFIG_PARTY_NAME_1,
    CONFIG_PARTY_NAME_2
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.nillion_client_helper import create_nillion_client

load_dotenv()

parser = argparse.ArgumentParser(
    description="Create a secret on the Nillion network with set read/retrieve permissions"
)
parser.add_argument(
    "--party_id_2",
    required=True,
    type=str,
    help="The 2nd Party's id",
)
parser.add_argument(
    "--store_id_1",
    required=True,
    type=str,
    help="Store ID of the 1st secret",
)
parser.add_argument(
    "--store_id_2",
    required=True,
    type=str,
    help="The 2nd Party's store id",
)

args = parser.parse_args()


async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")

    # 1st party computes on secrets
    userkey_path_1 = os.getenv("NILLION_WRITERKEY_PATH")
    userkey_1 = nillion.UserKey.from_file(userkey_path_1)
    client_1 = create_nillion_client(userkey_1)
    party_id_1 = client_1.party_id()


    # Bind the parties in the computation to the client to set inputs and output parties
    compute_bindings = nillion.ProgramBindings(CONFIG_PROGRAM_ID)
    compute_bindings.add_input_party(CONFIG_PARTY_NAME_1, party_id_1)
    compute_bindings.add_input_party(CONFIG_PARTY_NAME_2, args.party_id_2)
    compute_bindings.add_output_party(CONFIG_PARTY_NAME_1, party_id_1)

    store_id_1 = args.store_id_1
    store_id_2 = args.store_id_2

    print(f"Computing using program {CONFIG_PROGRAM_ID}")
    print(f"Party 1 secret store_id: {store_id_1}")
    print(f"Party 2 secret store_id: {store_id_2}")
    
    # Compute on the secret with 2 store ids. Note that there are no compute time secrets or public variables
    compute_id = await client_1.compute(
        cluster_id,
        compute_bindings,
        [store_id_1, store_id_2],
        nillion.Secrets({}),
        nillion.PublicVariables({}),
    )

    # Print compute result
    print(f"The computation was sent to the network. compute_id: {compute_id}")
    while True:
        compute_event = await client_1.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            print(f"🖥️  The result is {compute_event.result.value}")
            break
    

asyncio.run(main())
