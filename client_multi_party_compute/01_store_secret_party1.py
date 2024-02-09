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
    CONFIG_SECRETS_1
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.nillion_client_helper import create_nillion_client

load_dotenv()

# The 1st Party stores a secret
async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    userkey_path_1 = os.getenv("NILLION_WRITERKEY_PATH")
    userkey_1 = nillion.UserKey.from_file(userkey_path_1)
    client_1 = create_nillion_client(userkey_1)
    party_id_1 = client_1.party_id()
    user_id_1 = client_1.user_id()

    # 1st Party creates a secret
    stored_secret_1 = nillion.Secrets({
        key: nillion.SecretInteger(value)
        for key, value in CONFIG_SECRETS_1.items()
    })

    # 1st Party creates input bindings for the program
    secret_bindings_1 = nillion.ProgramBindings(CONFIG_PROGRAM_ID)
    secret_bindings_1.add_input_party(CONFIG_PARTY_NAME_1, party_id_1)

    # 1st Party stores a secret
    store_id_1 = await client_1.store_secrets(
        cluster_id, secret_bindings_1, stored_secret_1, None
    )
    secrets_string = ", ".join(f"{key}: {value}" for key, value in CONFIG_SECRETS_1.items())
    print(f"\n🎉1️⃣ Party {CONFIG_PARTY_NAME_1} stored {secrets_string} at store id: {store_id_1}")
    print("\n📋⬇️ Copy and run the following command to store the 2nd Party's secret")
    print(f"\npython3 02_store_secret_party2.py --user_id_1 {user_id_1} --store_id_1 {store_id_1}")


    

asyncio.run(main())
