import asyncio
import py_nillion_client as nillion
import os
import sys
import pytest

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()

# Store and retrieve a SecretArray using the Python Client
async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    userkey = getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    nodekey = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_1"))
    client = create_nillion_client(userkey, nodekey)

    # Create a SecretArray, a SecretInteger list
    secret_name = "my_array"
    secret_value = nillion.SecretArray([
        nillion.SecretInteger(1),
        nillion.SecretInteger(2),
        nillion.SecretInteger(3),
        nillion.SecretInteger(4),
        nillion.SecretInteger(5),
    ])

    secret_array = nillion.Secrets({
        secret_name: secret_value
    })

    # Store a SecretArray 
    # Notice that both bindings and permissions are set to None
    # Bindings need to be set to use secrets in programs
    # Permissions need to be set to allow users other than the secret creator to use the secret
    store_id = await client.store_secrets(
        cluster_id, None, secret_array, None
    )

    print(f"The secret is stored at store_id: {store_id}")

    # Retrieve the stored SecretArray
    result_tuple = await client.retrieve_secret(cluster_id, store_id, secret_name)

    print(f"The secret name as a uuid is {result_tuple[0]}")

    # This is the list of secret objects
    secret_results = result_tuple[1].value

    # Read the secret value of the 1st element in the secret array
    print(f"The secret array value at index 0 is {secret_results[0].value}")

    # Read all secret values in the secret array
    secret_array_values = [secret_value.value for secret_value in secret_results]
    print("The secret array values are:", secret_array_values)
    return secret_array_values

if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    result = await main()
    assert result == [1, 2, 3, 4, 5]
