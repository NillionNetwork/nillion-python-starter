from pdb import set_trace as bp
import argparse
import asyncio
import json
import py_nillion_client as nillion
import sys

parser = argparse.ArgumentParser(description='Retrieve a Secret owned by another peer from the Nillion network; this peer has read permissions')
parser.add_argument('--store_id', required=True, type=str, help='Store ID from the writer client store operation')
args = parser.parse_args()


async def main():
    with open(".nillion-config.json", "r") as fh:
        config = json.load(fh)

    # Path to the user keys
    reader_userkey_path = config["YOUR_READERKEY_PATH_HERE"]

    # Path to the node key generated in previous step
    nodekey_path = config["YOUR_NODEKEY_PATH_HERE"]

    # Bootnode multiadress from from run-local-cluster output
    bootnodes = [
        config["YOUR_BOOTNODE_MULTIADDRESS_HERE"]
    ]

    # This is the cluster id from run-local-cluster output
    cluster_id = config["YOUR_CLUSTER_ID_HERE"]

    nodekey = nillion.NodeKey.from_file(nodekey_path)

    reader = nillion.NillionClient(
        nodekey,
        bootnodes,
        nillion.ConnectionMode.relay(),
        nillion.UserKey.from_file(reader_userkey_path)
    )

    result = await reader.retrieve_secret(cluster_id, args.store_id, "fortytwo")
    print(f"🦄 Retrieved secret, value = {result[1].value}", file=sys.stderr)


asyncio.run(main())
