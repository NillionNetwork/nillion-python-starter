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
    description="Get the user id of a user by user key"
)
parser.add_argument(
    "--user_key",
    required=False,
    type=str,
    help="User key",
)
args = parser.parse_args()

async def main():
    if args.user_key:
        userkey = nillion.UserKey.from_base58(args.user_key)
    else:
        userkey_path = os.getenv("NILLION_USERKEY_PATH_PARTY_1")
        print(f"No user key specified. Using key in {userkey_path}")
        userkey = nillion.UserKey.from_file(userkey_path)
    
    print(f"user key: {userkey}")

    # create Nillion client for user
    user = create_nillion_client(userkey)
    user_user_id = user.user_id()
    print(f"user id: {user_user_id}")

asyncio.run(main())
