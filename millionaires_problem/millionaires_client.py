"""
Script to show how permissions can be added to secrets, to allow other parties the chance to compute on them
"""

import asyncio
import py_nillion_client as nillion
import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.nillion_client_helper import create_nillion_client

load_dotenv()

async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    print(cluster_id)
    # Instantiate Alice's client
    alice_user_key = nillion.UserKey.from_file(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    alice_node_key = nillion.NodeKey.from_file(os.getenv("NILLION_NODEKEY_PATH_PARTY_1"))
    alice_client = create_nillion_client(alice_user_key, alice_node_key)

    # Store the program Alice has written on the network
    program_name = "millionaires"
    program_mir_path = "/Users/davidtbutler/Documents/Git/nillion-python-starter-test-nodekey/millionaires_problem/millionaires.nada.bin"

    print(f"Storing program in the network: {program_name}")
    action_id = await alice_client.store_program(
        cluster_id, program_name, program_mir_path
    )
    program_id = alice_client.user_id() + "/" + program_name
    print("program_id is: ", program_id)

    # Instantiate Bob's client
    bob_user_key = nillion.UserKey.from_file(os.getenv("NILLION_USERKEY_PATH_PARTY_2"))
    bob_node_key = nillion.NodeKey.from_file(os.getenv("NILLION_NODEKEY_PATH_PARTY_2"))
    bob_client = create_nillion_client(bob_user_key, bob_node_key)
    print(bob_client)

    # Bob store's his secret on the network, giving permissions for Alice to compute her program over it
    bobs_salary = nillion.SecretInteger(10000)
    bobs_secret_salary = nillion.Secrets({"bobs_salary": bobs_salary})

    # Bob binds the storage of his secret to the program so it can be used as an input
    bindings = nillion.ProgramBindings(program_id)
    bindings.add_input_party("Party1", bob_client.party_id())

    # Bob gives permissions on the secret so Alice can compute the program over it
    bobs_permissions = nillion.Permissions.default_for_user(bob_client.user_id())
    bobs_permissions.add_compute_permissions({
        alice_client.user_id(): {program_id},
    })

    print(f"Storing Bob's secret: {bobs_secret_salary}")
    # Store the secret
    bobs_secret_salary_store_id = await bob_client.store_secrets(
        cluster_id, bindings, bobs_secret_salary, bobs_permissions
    )
    print(f"Bob's secret is stored with store id: {bobs_secret_salary_store_id}")

    # Instantiate Charlie's client
    charlie_user_key = nillion.UserKey.from_file(os.getenv("NILLION_USERKEY_PATH_PARTY_3"))
    charlie_node_key = nillion.NodeKey.from_file(os.getenv("NILLION_NODEKEY_PATH_PARTY_3"))
    charlie_client = create_nillion_client(charlie_user_key, charlie_node_key)

    # Bob store's his secret on the network, giving permissions for Alice to compute her program over it
    charlies_salary = nillion.SecretInteger(10000)
    charlies_secret_salary = nillion.Secrets({"charlies_salary": bobs_salary})

    # Charlie binds the storage of his secret to the program so it can be used as an input
    bindings.add_input_party("Party1", charlie_client.party_id())

    # Charlie gives permissions on the secret so Alice can compute the program over it
    charlies_permissions = nillion.Permissions.default_for_user(charlie_client.user_id())
    charlies_permissions.add_compute_permissions({
        alice_client.user_id(): {program_id},
    })

    print(f"Storing Charlie's secret: {charlies_secret_salary}")
    # Store the secret
    charlies_secret_salary_store_id = await charlie_client.store_secrets(
        cluster_id, bindings, charlies_secret_salary, charlies_permissions
    )
    print(f"Charlie's secret is stored with store id: {charlies_secret_salary_store_id}")

    sys.exit()
    nodekey = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_1"))
    client = create_nillion_client(userkey, nodekey)
    party_id = client.party_id()
    user_id = client.user_id()

    program_id=f"{user_id}/addition_simple"
    party_name="Party1"




    # for simplicity, we use the same payment configs for all parties in the computation
    payments_config = py_nillion_client.PaymentsConfig(
        rpc_endpoint="http://localhost:62204",
        private_key="df57089febbacf7ba0bc227dafbffa9fc08a93fdc68e1e42411a14efcf23656e",
        chain_id=31337,
        payments_address="5fc8d32690cc91d4c39d9d3abcbd16989f875707",
        blinding_factor_manager_address="a513e6e4b8f2a923d98304ec87f64353c4d5c853")

    # This is the program id from previous step.
    program_id = "51M9Me4fvZtnsG1DLb11yuTJUp3vwbMix8r2ooEWgwJyQp8Zk42iK7Nt1Hakc6fc7nsFYKjZDv9bXvZt4sNh7HV6/multi_input_arith"

    # get keys for 3 parties, party 1, 2 and the owner of the computation (user and node, no suffix numbers)
    owner_user_key_path = "./user.key"
    owner_node_key_path = "./node.key"
    party1_user_key_path = "./user1.key"
    party1_node_key_path = "./node1.key"
    party2_user_key_path = "./user2.key"
    party2_node_key_path = "./node2.key"

    owner_user_key = py_nillion_client.UserKey.from_file(owner_user_key_path)
    owner_node_key = py_nillion_client.NodeKey.from_file(owner_node_key_path)
    party1_user_key = py_nillion_client.UserKey.from_file(party1_user_key_path)
    party1_node_key = py_nillion_client.NodeKey.from_file(party1_node_key_path)
    party2_user_key = py_nillion_client.UserKey.from_file(party2_user_key_path)
    party2_node_key = py_nillion_client.NodeKey.from_file(party2_node_key_path)

    # Bootnode multiadress from previous step
    bootnodes = [
        "/ip4/127.0.0.1/tcp/45564/ws/p2p/12D3KooWDGA8YRDNPXKrLris2arLocR6iqKT8Ff2hJkFJ6GZfG9E"
    ]

    # Cluster id from previous step
    cluster_id = "95b1cc65-9599-4556-bf3e-8bd2aec4670c"

    # Create Nillion Client for computation owner
    owner_client = py_nillion_client.NillionClient(
        owner_node_key,
        bootnodes,
        py_nillion_client.ConnectionMode.relay(),
        owner_user_key,
        payments_config=payments_config
    )

    # Create Nillion Client for party 1
    party1_client = py_nillion_client.NillionClient(
        party1_node_key,
        bootnodes,
        py_nillion_client.ConnectionMode.relay(),
        party1_user_key,
        payments_config=payments_config
    )

    # Create Nillion Client for party 2
    party2_client = py_nillion_client.NillionClient(
        party2_node_key,
        bootnodes,
        py_nillion_client.ConnectionMode.relay(),
        party2_user_key,
        payments_config=payments_config
    )

    # SecretInteger for party1
    int1 = py_nillion_client.SecretInteger(3)
    int2 = py_nillion_client.SecretInteger(5)

    # store party 1's secret and give permissions to the computing party
    party1_secrets_to_be_stored = py_nillion_client.Secrets({"int1": int1, "int2": int2})

    # We bind the storage of the secret to the circuit and the concrete party
    bindings = py_nillion_client.ProgramBindings(program_id)
    bindings.add_input_party("Party1", party1_client.party_id())

    # Give permissions to owner to compute with my vote
    party1_permissions = py_nillion_client.Permissions.default_for_user(party1_client.user_id())
    party1_permissions.add_compute_permissions({
        owner_client.user_id(): {program_id},
    })

    print(f"Storing secret: {party1_secrets_to_be_stored}")
    # Store the secret
    party1_store_id = await party1_client.store_secrets(
        cluster_id, bindings, party1_secrets_to_be_stored, party1_permissions
    )

    # SecretInteger for party2
    int3 = py_nillion_client.SecretInteger(56)

    party2_secrets_to_be_stored = py_nillion_client.Secrets({"int3": int3})

    # We bind the storage of the secret to the circuit and the concrete party
    bindings.add_input_party("Party2", party2_client.party_id())

    # Give permissions to owner to compute with my vote
    party2_permissions = py_nillion_client.Permissions.default_for_user(party2_client.user_id())
    party2_permissions.add_compute_permissions({
        owner_client.user_id(): {program_id},
    })

    print(f"Storing secret: {party2_secrets_to_be_stored}")
    # Store the secret
    party2_store_id = await party2_client.store_secrets(
        cluster_id, bindings, party2_secrets_to_be_stored, party2_permissions
    )

    bindings.add_output_party("ResultParty", owner_client.party_id())
    print(f"Computing using program {program_id}")
    print(f"Stored secret by party 1 being used: {party1_store_id}")
    print(f"Stored secret by party 2 being used: {party2_store_id}")
    # do the computation
    compute_id = await owner_client.compute(
        cluster_id,
        bindings,
        [party1_store_id, party2_store_id],
        py_nillion_client.Secrets({}),
        py_nillion_client.PublicVariables({}),
    )

    print(f"Computation sent to the network, compute_id = {compute_id}")
    print("Waiting computation response")
    while True:
        event = await owner_client.next_compute_event()
        if isinstance(event, py_nillion_client.ComputeFinishedEvent):
            print(
                f"Received computation result for {event.uuid}, value = {event.result.value}"
            )
            break

asyncio.run(main())