import os
from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
load_dotenv("/Users/davidtbutler/Library/Application Support/nillion.nillion/nillion-devnet.env")

# replace this with your program_id
CONFIG_PROGRAM_NAME="addition_simple_multi_party_3"

# 1st party
CONFIG_PARTY_1={
    "seed": "party_1_seed",
    "nodekey_alternate_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_4"),
    "party_name": "Party1",
    "secrets": {
        "my_int1": 1,
    }
}

# N other parties
CONFIG_N_PARTIES=[
    {
        "seed": "party_2_seed",
        "party_name": "Party2",
        "secret_name": "my_int2",
        "secret_value": 5,
    },
    {
        "seed": "party_3_seed",
        "party_name": "Party3",
        "secret_name": "my_int3",
        "secret_value": 2,
    },
]