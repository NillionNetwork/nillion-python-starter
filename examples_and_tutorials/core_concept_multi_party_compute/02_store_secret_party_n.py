import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
import pytest

from dotenv import load_dotenv
from config import (
    CONFIG_PROGRAM_NAME,
    CONFIG_N_PARTIES
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()

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
    program_id=f"{args.user_id_1}/{CONFIG_PROGRAM_NAME}"
    
    # start a list of store ids to keep track of stored secrets
    store_ids = []
    party_ids = []

    for party_info in CONFIG_N_PARTIES:
        client_n = create_nillion_client(
            getUserKeyFromFile(party_info["userkey_file"]), 
            getNodeKeyFromFile(party_info["nodekey_file"])
        )
        party_id_n = client_n.party_id
        user_id_n = client_n.user_id
        party_name = party_info["party_name"]
        secret_name = party_info["secret_name"]
        secret_value = party_info["secret_value"]

        # Create a secret for the current party
        stored_secret = nillion.Secrets({
            secret_name: nillion.SecretInteger(secret_value)
        })

        # Create input bindings for the program
        secret_bindings = nillion.ProgramBindings(program_id)
        secret_bindings.add_input_party(party_name, party_id_n)

        # Create permissions object
        permissions = nillion.Permissions.default_for_user(user_id_n)

        # Give compute permissions to the first party
        compute_permissions = {
            args.user_id_1: {program_id},
        }
        permissions.add_compute_permissions(compute_permissions)

        # Store the permissioned secret
        store_id = await client_n.store_secrets(
            cluster_id, secret_bindings, stored_secret, permissions
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
