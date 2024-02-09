from pdb import set_trace as bp
import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
from dotenv import load_dotenv
from config import (
    CONFIG_PROGRAM_ID,
    CONFIG_PARTY_NAME_2,
    CONFIG_SECRETS_2
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.nillion_client_helper import create_nillion_client

load_dotenv()

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

args = parser.parse_args()

# The 2nd Party stores a secret
async def main():
    user_id_1=args.user_id_1
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    userkey_path_2 = os.getenv("NILLION_READERKEY_PATH")
    userkey_2 = nillion.UserKey.from_file(userkey_path_2)
    client_2 = create_nillion_client(userkey_2)
    party_id_2 = client_2.party_id()
    user_id_2 = client_2.user_id()

    # 2nd Party creates a secret
    stored_secret_2 = nillion.Secrets({
        key: nillion.SecretInteger(value)
        for key, value in CONFIG_SECRETS_2.items()
    })
    
    # 2nd Party creates input bindings for the program
    secret_bindings_2 = nillion.ProgramBindings(CONFIG_PROGRAM_ID)
    secret_bindings_2.add_input_party(CONFIG_PARTY_NAME_2, party_id_2)

    # 2nd Party creates a permissions object and gives themself default permissions
    permissions = nillion.Permissions.default_for_user(user_id_2)
    
    # 2nd Party gives 1st Party (by user id) compute permissions to use the secret in a specific program id
    compute_permissions = {
        user_id_1: {CONFIG_PROGRAM_ID},
    }
    permissions.add_compute_permissions(compute_permissions)

    # 2nd party stores the permissioned secret
    store_id_2 = await client_2.store_secrets(
        cluster_id, secret_bindings_2, stored_secret_2, permissions
    )

    secrets_string = ", ".join(f"{key}: {value}" for key, value in CONFIG_SECRETS_2.items())
    print(f"\n🎉2️⃣ Party {CONFIG_PARTY_NAME_2} stored {secrets_string} at store id: {store_id_2}")
    print("\n📋⬇️ Copy and run the following command to run multi party computation using the secrets")
    print(f"\npython3 03_multi_party_compute.py --party_id_2 {party_id_2} --store_id_1 {args.store_id_1} --store_id_2 {store_id_2}")


    

asyncio.run(main())
