import os
from dotenv import load_dotenv
load_dotenv()

# replace this with your program_id
CONFIG_PROGRAM_NAME="millionaires_multi_output"

# 1st party
CONFIG_PARTY_1={
    "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_1"),
    "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_1"),
    "nodekey_alternate_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_4"),
    "party_name": "Alice",
    "secrets": {
        "alice_salary": 1,
    }
}

# N other parties
CONFIG_N_PARTIES=[
    {
        "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_2"),
        "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_2"),
        "party_name": "Bob",
        "secret_name": "bob_salary",
        "secret_value": 5,
        "is_output_party": True
    },
    {
        "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_3"),
        "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_3"),
        "party_name": "Charlie",
        "secret_name": "charlie_salary",
        "secret_value": 2,
        "is_output_party": True
    },
]