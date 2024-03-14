import os
import py_nillion_client as nillion
from dotenv import load_dotenv
load_dotenv()

def getUserKeyFromFile(userkey_filepath):
    return nillion.UserKey.from_file(userkey_filepath)

def getNodeKeyFromFile(nodekey_filepath):
    return nillion.NodeKey.from_file(nodekey_filepath)

# replace this with your program_id
CONFIG_PROGRAM_ID="5yjjLMczHWPefgNNNivaG1d9ikkbaM1B8KNMU7Z9tCB8vD4ssKGadJGFQMoJRcTxunb97wUic6kAM92BG78uNdcZ/addition_simple_multi_party_3"

# 1st party
CONFIG_PARTY_NAME_PARTY_1="Party1"
CONFIG_SECRETS_PARTY_1={
    "my_int1": 10,
}

CONFIG_PARTY_1={
    "userkey": getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_1")),
    "nodekey": getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_1")),
    "party_name": "Party1",
    "secrets": {
        "my_int1": 10,
    }
}

# N other parties
CONFIG_N_PARTIES=[
    {
        "userkey": getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_2")),
        "nodekey": getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_2")),
        "party_name": "Party2",
        "secret_name": "my_int2",
        "secret_value": 5,
    },
    {
        "userkey": getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_3")),
        "nodekey": getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_3")),
        "party_name": "Party3",
        "secret_name": "my_int3",
        "secret_value": 2,
    },
]