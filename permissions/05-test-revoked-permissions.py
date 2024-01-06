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
    description="Check that retrieval permissions on a Secret have been revoked"
)
parser.add_argument(
    "--store_id",
    required=True,
    type=str,
    help="Store ID from the writer client store operation",
)
args = parser.parse_args()


async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    reader_userkey_path = os.getenv("NILLION_READERKEY_PATH")
    reader_userkey = nillion.UserKey.from_file(reader_userkey_path)
    
    # Reader Nillion client
    reader = create_nillion_client(reader_userkey)
    reader_user_id = reader.user_id()

    try:
        secret_name = "fortytwo"
        result = await reader.retrieve_secret(cluster_id, args.store_id, secret_name)
        print(f"⛔ FAIL: {reader_user_id} user id with revoked permissions was allowed to access secret", file=sys.stderr)
    except TypeError as e:
        if str(e) == "the user is not authorized to access the secret":
            print(f"🦄 Success: After user permissions were revoked, {reader_user_id} was not allowed to access secret", file=sys.stderr)
            pass
        else:
            raise(e)


asyncio.run(main())
