import asyncio
import py_nillion_client as nillion
import os
import sys
import pytest

from dotenv import load_dotenv
from config import (
    CONFIG_PROGRAM_NAME,
    CONFIG_PARTY_1
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()

# The 1st Party stores a secret
async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    client_1 = create_nillion_client(
        getUserKeyFromFile(CONFIG_PARTY_1["userkey_file"]), getNodeKeyFromFile(CONFIG_PARTY_1["nodekey_file"])
    )
    party_id_1 = client_1.party_id
    user_id_1 = client_1.user_id


    program_mir_path=f"../../programs-compiled/{CONFIG_PROGRAM_NAME}.nada.bin"

    # 1st Party stores program
    action_id = await client_1.store_program(
        cluster_id, CONFIG_PROGRAM_NAME, program_mir_path
    )

    program_id=f"{user_id_1}/{CONFIG_PROGRAM_NAME}"
    print('Stored program. action_id:', action_id)
    print('Stored program_id:', program_id)


    # 1st Party creates a secret
    stored_secret_1 = nillion.Secrets({
        key: nillion.SecretInteger(value)
        for key, value in CONFIG_PARTY_1["secrets"].items()
    })

    # 1st Party creates input bindings for the program
    secret_bindings_1 = nillion.ProgramBindings(program_id)
    secret_bindings_1.add_input_party(CONFIG_PARTY_1["party_name"], party_id_1)

    # 1st Party stores a secret
    store_id_1 = await client_1.store_secrets(
        cluster_id, secret_bindings_1, stored_secret_1, None
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
