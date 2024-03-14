import os
import py_nillion_client as nillion
from helpers.nillion_payments_helper import create_payments_config

def create_nillion_client(userkey):
    nodekey_path = os.getenv("NILLION_NODEKEY_PATH_PARTY_1")
    bootnodes = [os.getenv("NILLION_BOOTNODE_MULTIADDRESS")]
    nodekey = nillion.NodeKey.from_file(nodekey_path)
    payments_config = create_payments_config()

    return nillion.NillionClient(
        nodekey,
        bootnodes,
        nillion.ConnectionMode.relay(),
        userkey,
        payments_config,
    )