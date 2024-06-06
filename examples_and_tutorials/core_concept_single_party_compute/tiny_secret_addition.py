import asyncio
import os
import sys
import pytest

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()


# Complete the 🎯 TODOs to store the tiny_secret_addition program in the network, store secrets, and compute
async def main():
    # 0. The bootstrap-local-environment.sh script put nillion-devnet config variables into the .env file
    # Get cluster_id, user_key, and node_key from the .env file
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_GRPC")
    chain_id = os.getenv("NILLION_CHAIN_ID")
    userkey = getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    nodekey = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_1"))

    # 🎯 TODO 1. Initialize NillionClient against nillion-devnet
    # Create Nillion Client for user
    client = create_nillion_client(userkey, nodekey)

    # 🎯 TODO 2. Get the user id and party id from NillionClient

    # 🎯 TODO 3. Create a payments config, payments client and payments wallet then pay for and store a compiled Nada program in the network
    # Set the program name
    program_name = "tiny_secret_addition"
    # Set the path to the compiled program
    program_mir_path = f"../../programs-compiled/{program_name}.nada.bin"
    # Create payments config
    # Pay to store the program
    # Store program
    # Create a variable for the program_id, which is the {user_id}/{program_name}

    # 🎯 TODO 4. Create the 1st secret with bindings to the program
    # Create a secret named "my_int1" with any value, ex: 500
    # Create secret bindings object to bind the secret to the program and set the input party
    # Set the input party for the secret
    # The party name needs to match the party name that is storing "my_int1" in the program
    # Set permissions for the client to compute on the program

    # 🎯 TODO 5. Store the secret in the network and print the returned store_id
    # Pay to store the secret
    # Store a secret, passing in the receipt from payment

    # 🎯 TODO 6. Create compute bindings to set input and output parties

    # 🎯 TODO 7. Pay for and compute on the program with 1st secret from the network, and the 2nd secret, provided at compute time
    # Add my_int2, the 2nd secret at computation time
    # Pay for the compute
    # Compute on the secret

    # 🎯 TODO 8. Print the computation result


if __name__ == "__main__":
    asyncio.run(main())


@pytest.mark.asyncio
async def test_main():
    pass
