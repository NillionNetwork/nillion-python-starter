import asyncio
import json
import py_nillion_client as nillion


async def main():
    with open(".nillion-config.json", "r") as fh:
        config = json.load(fh)

    # Path to the user keys
    reader_userkey_path = config["YOUR_READERKEY_PATH_HERE"]

    # Path to the node key generated in previous step
    nodekey_path = config["YOUR_NODEKEY_PATH_HERE"]

    # Bootnode multiadress from from run-local-cluster output
    bootnodes = [config["YOUR_BOOTNODE_MULTIADDRESS_HERE"]]

    # This is the cluster id from run-local-cluster output
    cluster_id = config["YOUR_CLUSTER_ID_HERE"]

    nodekey = nillion.NodeKey.from_file(nodekey_path)

    reader = nillion.NillionClient(
        nodekey,
        bootnodes,
        nillion.ConnectionMode.relay(),
        nillion.UserKey.from_file(reader_userkey_path),
    )

    print(reader.user_id())


asyncio.run(main())
