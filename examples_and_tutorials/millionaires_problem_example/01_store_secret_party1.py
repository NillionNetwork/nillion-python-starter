import asyncio
import os
import sys
import pytest

from dotenv import load_dotenv
from config import (
    CONFIG_PARTY_1
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()

# Alice stores the millionaires program in the network
async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    client_alice = create_nillion_client(
        getUserKeyFromFile(CONFIG_PARTY_1["userkey_file"]), getNodeKeyFromFile(CONFIG_PARTY_1["nodekey_file"])
    )

    millionaires_program_name = "millionaires"
    
    # Note: check out the code for the full millionaires program in the programs folder
    program_mir_path = "millionaires.nada.bin"

    # Store millionaires program in the network
    print(f"Storing program in the network: {millionaires_program_name}")
    await client_alice.store_program(
        cluster_id, millionaires_program_name, program_mir_path
    )

    user_id_alice = client_alice.user_id
    program_id = f"{user_id_alice}/{millionaires_program_name}"

    print(f"Alice stores millionaires program at program_id: {program_id}")
    print(f"Alice tells Bob and Charlie her user_id and the millionaires program_id")

    print("\n📋⬇️ Copy and run the following command to store Bob and Charlie's salaries in the network")
    print(f"\npython3 02_store_secret_party_n.py --user_id_1 {user_id_alice} --program_id {program_id}")
    return [user_id_alice, program_id]

if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    pass
