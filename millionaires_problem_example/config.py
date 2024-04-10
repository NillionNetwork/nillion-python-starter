import os
import py_nillion_client as nillion
from dotenv import load_dotenv
load_dotenv()

# Alice
CONFIG_PARTY_1={
    "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_1"),
    "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_1"),
    "nodekey_alternate_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_4"),
    "party_name": "Alice",
    "secret_name": "alice_salary",
    "secret_value": 10000,
}

# Bob and Charlie
CONFIG_N_PARTIES=[
    {
        "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_2"),
        "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_2"),
        "party_name": "Bob",
        "secret_name": "bob_salary",
        "secret_value": 8000,
    },
    {
        "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_3"),
        "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_3"),
        "party_name": "Charlie",
        "secret_name": "charlie_salary",
        "secret_value": 12000,
    },
]