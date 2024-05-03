import os
from dotenv import load_dotenv
load_dotenv()

# replace this with your program_id
CONFIG_PROGRAM_NAME="addition_simple_multi_party_3"

# 1st party
CONFIG_PARTY_1={
    "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_1"),
    "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_1"),
    "nodekey_alternate_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_4"),
    "party_name": "Party1",
    "secrets": {
        "my_int1": 1,
    }
}

# N other parties
CONFIG_N_PARTIES=[
    {
        "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_2"),
        "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_2"),
        "party_name": "Party2",
        "secret_name": "my_int2",
        "secret_value": 5,
    },
    {
        "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_3"),
        "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_3"),
        "party_name": "Party3",
        "secret_name": "my_int3",
        "secret_value": 2,
    },
]