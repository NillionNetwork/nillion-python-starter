from pdb import set_trace as bp
import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
from dotenv import load_dotenv
from nillion_client_helper import create_nillion_client
load_dotenv()

parser = argparse.ArgumentParser(
    description="Revoke user read/retrieve permissions from a secret on the Nillion network"
)
parser.add_argument(
    "--store_id",
    required=True,
    type=str,
    help="Store ID from the writer client store operation",
)
parser.add_argument(
    "--revoked_user_id",
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

    # Create new permissions object to rewrite permissions (reader no longer has retrieve permission)
    new_permissions = nillion.Permissions.default_for_user(writer.user_id())
    result = (
        "allowed"
        if new_permissions.is_retrieve_allowed(args.revoked_user_id)
        else "not allowed"
    )
    if result != "not allowed":
        raise Exception("failed to create valid permissions object")

    # Update the permission
    print(f"ℹ️ Updating permissions for secret: {args.store_id}.") 
    print(f"ℹ️ Reset permissions so that user id {args.revoked_user_id} is {result} to retrieve object.", file=sys.stderr)
    await writer.update_permissions( cluster_id, args.store_id , new_permissions)

    print("\n\nRun the following command to test that permissions have been properly revoked")
    print(f"\n📋  python3 05-test-revoked-permissions  --store_id {args.store_id}")


asyncio.run(main())
