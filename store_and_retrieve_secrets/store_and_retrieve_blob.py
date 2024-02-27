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

# Store and retrieve a SecretBlob using the Python Client
async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    userkey_path = os.getenv("NILLION_WRITERKEY_PATH")
    userkey = nillion.UserKey.from_file(userkey_path)
    client = create_nillion_client(userkey)

    # Create a SecretBlob
    secret_name = "my_blob"

    # create a bytearray from the string using UTF-8 encoding
    secret_value = bytearray("gm, builder!", "utf-8")
    secret_integer = nillion.Secrets({
        secret_name: nillion.SecretBlob(secret_value),
    })

    # Store a SecretBlob 
    # Notice that both bindings and permissions are set to None
    # Secrets of type SecretBlob don't need bindings because they aren't used in programs
    # Permissions need to be set to allow users other than the secret creator to use the secret
    store_id = await client.store_secrets(
        cluster_id, None, secret_integer, None
    )

    print(f"The secret is stored at store_id: {store_id}")

    result_tuple = await client.retrieve_secret(cluster_id, store_id, secret_name)
    print(f"The secret name as a uuid is {result_tuple[0]}")

    decoded_secret_value = result_tuple[1].value.decode('utf-8')
    print(f"The secret value is '{decoded_secret_value}'")

asyncio.run(main())
