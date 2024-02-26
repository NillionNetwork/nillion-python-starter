# replace this with your program_id
CONFIG_PROGRAM_ID="4ooSsZY3xTeSjdkyt48bmeDE988kTUHsBhNpDiXU5BCfyR5KqR75DVxYY7etRULRDgWgt6VKdTZ61barogrYDGja/addition_simple_multi_party"

# 1st party
CONFIG_PARTY_NAME_1="Party1"
CONFIG_SECRETS_1={
    "my_int1": 10,
}

# N other parties
N_PARTIES=[
    {
        "party_name": "Party2",
        "secret_name": "my_int2",
        "secret_value": 5,
    },
]