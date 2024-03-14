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

parser = argparse.ArgumentParser(
    description="Create a secret on the Nillion network with set read/retrieve permissions"
)
parser.add_argument(
    "--retriever_user_id",
    required=True,
    type=str,
    help="User ID of the reader python client (derived from user key)",
)
args = parser.parse_args()


async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    userkey_path_party_1 = os.getenv("NILLION_USERKEY_PATH_PARTY_1")
    userkey_party_1 = nillion.UserKey.from_file(userkey_path_party_1)

    # Writer Nillion client
    writer = create_nillion_client(userkey_party_1)
    writer_user_id = writer.user_id()
    print(writer_user_id, args.retriever_user_id)

    # Writer gives themself default permissions
    permissions = nillion.Permissions.default_for_user(writer_user_id)
    # Writer gives the reader permission to read/retrieve secret
    permissions.add_retrieve_permissions(set([args.retriever_user_id, writer_user_id]))

    result = (
        "allowed"
        if permissions.is_retrieve_allowed(args.retriever_user_id)
        else "not allowed"
    )
    if result == "not allowed":
        raise Exception("failed to set permissions")
    
    print(f"ℹ️ Permissions set: Reader {args.retriever_user_id} is {result} to retrieve the secret")

    secret_name_1 = "my_int1"
    secret_1 = nillion.SecretInteger(10)

    secret_name_2 = "my_int2"
    secret_2 = nillion.SecretInteger(32)
    secrets_object = nillion.Secrets({secret_name_1: secret_1, secret_name_2: secret_2})

    # Writer stores the permissioned secret, resulting in the secret's store id
    print(f"ℹ️  Storing permissioned secret: {secrets_object}")
    store_id = await writer.store_secrets(
        cluster_id, None, secrets_object, permissions
    )

    print("ℹ️ STORE ID:", store_id)
    print("\n\nRun the following command to retrieve the secret by store id as the reader")
    print(f"\n📋 python3 03-retrieve-secret.py --store_id {store_id}")


asyncio.run(main())
