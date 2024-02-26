from pdb import set_trace as bp
import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.nillion_client_helper import create_nillion_client

load_dotenv()

# Store and retrieve a SecretArray using the Python Client
async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    userkey_path = os.getenv("NILLION_WRITERKEY_PATH")
    userkey = nillion.UserKey.from_file(userkey_path)
    client = create_nillion_client(userkey)

    # Create a SecretArray, a SecretInteger list
    secret_name = "my_array"
    secret_value = nillion.SecretArray([
        nillion.SecretInteger(1),
        nillion.SecretInteger(2),
        nillion.SecretInteger(3),
        nillion.SecretInteger(4),
        nillion.SecretInteger(5),
    ])

    secret_array_length = len(secret_value)
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
    result = await client.retrieve_secret(cluster_id, store_id, secret_name)

    # This is the list of secret objects
    secret_results = result[1].value

    # Read the secret value of the 1st element in the secret array
    print(f"The 1st secret array value is {secret_results[0].value}")

    # Read all secret values in the secret array
    secret_array_values = [secret_value.value for secret_value in secret_results]
    print("The secret array values are:", secret_array_values)

asyncio.run(main())
