import asyncio
import py_nillion_client as nillion
import os
import sys
import pytest

from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from helpers.nillion_client_helper import create_nillion_client, pay, create_payments_config

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")

# Store and retrieve a SecretBlob using the Python Client
async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    seed = "my_seed"
    userkey = UserKey.from_seed((seed))
    nodekey = NodeKey.from_seed((seed))
    client = create_nillion_client(userkey, nodekey)

    # Create payments config and set up Nillion wallet with a private key to pay for operations
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))), prefix="nillion"
    )

    ##### STORE SECRET
    print('-----STORE SECRET')

    # Create a SecretBlob
    secret_name = "my_blob"

    # create a bytearray from the string using UTF-8 encoding
    secret_value = bytearray("gm, builder!", "utf-8")

    # Create a secret
    stored_secret = nillion.Secrets({
        secret_name: nillion.SecretBlob(secret_value),
    })

    # Create a permissions object to attach to the stored secret 
    permissions = nillion.Permissions.default_for_user(client.user_id)

    # Get cost quote, then pay for operation to store the secret
    receipt_store = await pay(
        client, nillion.Operation.store_values(stored_secret), payments_wallet, payments_client, cluster_id
    )

    # Store a secret, passing in the receipt that shows proof of payment
    store_id = await client.store_values(
        cluster_id, stored_secret, permissions, receipt_store
    )

    print(f"The secret is stored at store_id: {store_id}")

    ##### RETRIEVE SECRET
    print('-----RETRIEVE SECRET')

    # Get cost quote, then pay for operation to retrieve the secret
    receipt_retrieve = await pay(
        client, nillion.Operation.retrieve_value(), payments_wallet, payments_client, cluster_id
    )

    result_tuple = await client.retrieve_value(cluster_id, store_id, secret_name, receipt_retrieve)
    print(f"The secret name as a uuid is {result_tuple[0]}")

    decoded_secret_value = result_tuple[1].value.decode('utf-8')
    print(f"The secret value is '{decoded_secret_value}'")
    return decoded_secret_value

if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    result = await main()
    assert result == 'gm, builder!'
