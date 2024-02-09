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
    description="Use read permissions to retrieve a secret owned by another user on the Nillion network"
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

    reader_userkey_file = os.getenv("NILLION_WRITERKEY_PATH")
    reader_userkey = nillion.UserKey.from_file(reader_userkey_file)

    # Reader Nillion client
    reader = create_nillion_client(reader_userkey)
    reader_user_id = reader.user_id()

    secret_name_1 = "my_int1"
    # secret_name_2 = "my_int2"

    # Reader retrieves the named secret by store id
    print(f"Retrieving secret as reader: {reader_user_id}")
    result_1 = await reader.retrieve_secret(cluster_id, args.store_id, secret_name_1)
    # result_2 = await reader.retrieve_secret(cluster_id, args.store_id, secret_name_2)

    print(f"🦄 Retrieved {secret_name_1} secret, value = {result_1[1].value}", file=sys.stderr)
    # print(f"🦄 Retrieved {secret_name_2} secret, value = {result_2[1].value}", file=sys.stderr)


asyncio.run(main())
