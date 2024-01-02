from pdb import set_trace as bp
import argparse
import asyncio
import py_nillion_client as nillion
import os
from dotenv import load_dotenv
from nillion_client_helper import create_nillion_client

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
    writer_userkey_path = os.getenv("NILLION_WRITERKEY_PATH")
    writer_userkey = nillion.UserKey.from_file(writer_userkey_path)

    # Writer Nillion client
    writer = create_nillion_client(writer_userkey)

    # Writer gives themself default permissions
    permissions = nillion.Permissions.default_for_user(writer.user_id())

    # Writer gives the reader permission to read/retrieve secret
    permissions.add_retrieve_permissions(set([args.retriever_user_id]))
    result = (
        "allowed"
        if permissions.is_retrieve_allowed(args.retriever_user_id)
        else "not allowed"
    )
    if result == "not allowed":
        raise Exception("failed to set permissions")
    
    print(f"ℹ️ Permissions set: Reader {args.retriever_user_id} is {result} to retrieve the secret")

    secret_name = "fortytwo"
    secret = nillion.SecretInteger(42)
    secrets_object = nillion.Secrets({secret_name: secret})

    # Writer stores the permissioned secret, resulting in the secret's store id
    print(f"ℹ️  Storing permissioned secret: {secrets_object}")
    store_id = await writer.store_secrets(
        cluster_id, None, secrets_object, permissions
    )

    print("ℹ️ STORE ID:", store_id)
    print("\n\nRun the following command to retrieve the secret by store id as the reader")
    print(f"\n📋 python3 03-retrieve-secret.py --store_id {store_id}")


asyncio.run(main())
