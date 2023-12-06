from pdb import set_trace as bp
import argparse
import asyncio
import json
import py_nillion_client as nillion
import os
import sys

parser = argparse.ArgumentParser(
    description="Create a Secret on the Nillion network; set with peer read permissions"
)
parser.add_argument(
    "--reader_user_id",
    required=True,
    type=str,
    help="Peer ID of the reader python client (derived from user key)",
)
args = parser.parse_args()


async def main():
    with open(os.environ["NILLION_CONFIG"], "r") as fh:
        config = json.load(fh)

    # Path to the user keys
    writer_userkey_path = config["YOUR_WRITERKEY_PATH_HERE"]

    # Path to the node key generated in previous step
    nodekey_path = config["YOUR_NODEKEY_PATH_HERE"]

    # Bootnode multiadress from from run-local-cluster output
    bootnodes = [config["YOUR_BOOTNODE_MULTIADDRESS_HERE"]]

    # This is the cluster id from run-local-cluster output
    cluster_id = config["YOUR_CLUSTER_ID_HERE"]

    payments_config = nillion.PaymentsConfig(
        config["YOUR_BLOCKCHAIN_RPC_ENDPOINT"],
        config["YOUR_WALLET_PRIVATE_KEY"],
        int(config["YOUR_CHAIN_ID"]),
        config["YOUR_PAYMENTS_SC_ADDRESS"],
        config["YOUR_BLINDING_FACTORS_MANAGER_SC_ADDRESS"],
    )

    nodekey = nillion.NodeKey.from_file(nodekey_path)

    writer = nillion.NillionClient(
        nodekey,
        bootnodes,
        nillion.ConnectionMode.relay(),
        nillion.UserKey.from_file(writer_userkey_path),
        payments_config
    )

    print(f"ℹ️  adding permissions for [{args.reader_user_id}]", file=sys.stderr)
    writer_permission = nillion.Permissions.default_for_user(writer.user_id())
    writer_permission.add_retrieve_permissions(set([args.reader_user_id]))
    result = (
        "allowed"
        if writer_permission.is_retrieve_allowed(args.reader_user_id)
        else "not allowed"
    )
    if result == "not allowed":
        raise Exception("failed to set permissions")

    to_be_store_secrets = nillion.Secrets({"fortytwo": nillion.SecretInteger(42)})

    # Store the secret
    print(f"ℹ️  storing secret: {to_be_store_secrets}", file=sys.stderr)
    store_id = await writer.store_secrets(
        cluster_id, None, to_be_store_secrets, writer_permission
    )
    print(store_id)


asyncio.run(main())
