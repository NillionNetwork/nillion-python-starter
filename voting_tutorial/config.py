import os
from dotenv import load_dotenv
load_dotenv()

CONFIG = {
    "nr_candidates": 2,
    "nr_voters": 3,
}

CONFIG_CANDIDATES=[
    "Dave",
    "Emma"
]


# Alice
CONFIG_PARTY_1={
    "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_1"),
    "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_1"),
    "party_name": "Alice",
    "party_role": "Voter0",
    "secret_votes": {
        "v0_c0": 1,
        "v0_c1": 2,
    },
}

# Bob and Charlie
CONFIG_N_PARTIES=[
    {
        "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_2"),
        "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_2"),
        "party_name": "Bob",
        "party_role": "Voter1",
        "secret_votes": {
            "v1_c0": 1,
            "v1_c1": 2,
        },
    },
    {
        "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_3"),
        "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_3"),
        "party_name": "Charlie",
        "party_role": "Voter2",
        "secret_votes": {
            "v2_c0": 2,
            "v2_c1": 1,
        },
    },
]