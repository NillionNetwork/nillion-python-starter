import asyncio
import py_nillion_client as nillion
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()

async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")

    ### Create Alice's client, store the program & add bind Alice as input party to the program
    alice_user_key = getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    alice_node_key = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_1"))
    alice_client = create_nillion_client(alice_user_key, alice_node_key)
    alice_user_id = alice_client.user_id()

    program_name = "millionaires"
    program_mir_path = "/Users/davidtbutler/Documents/Git/nillion-python-starter-test-nodekey/millionaires_problem/millionaires.nada.bin"

    # Store program in the Network
    print("Storing program in the network: {program_name}")
    action_id = await alice_client.store_program(
        cluster_id, program_name, program_mir_path
    )

    program_id = alice_user_id + "/" + program_name

    print(f"Uploaded program with program id: {program_id}")

    # Bind Alice as input party to program
    bindings = nillion.ProgramBindings(program_id)
    bindings.add_input_party("Party1", alice_client.party_id())

    ### Instantitate Bob's client,  store his secret & give permissions and bindings for Alice to compute her program on it
    bob_user_key = getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_2"))
    bob_node_key = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_2"))
    bob_client = create_nillion_client(bob_user_key, bob_node_key)
    bob_user_id = bob_client.user_id()

    # Bob creates his secret
    bobs_salary_input = nillion.SecretInteger(10000)
    bobs_secret_salary_object = nillion.Secrets({
        "input2": bobs_salary_input,
    })

    # Bob adds permissions for Alice to compute her program on his secret
    permissions = nillion.Permissions.default_for_user(bob_user_id)
    permissions.add_compute_permissions({alice_user_id: {program_id}})
    bindings.add_input_party("Party2", bob_client.party_id())

    print(f"Storing Bob's secret")
    # Writer stores the permissioned secret, resulting in the secret's store id
    bob_store_id = await bob_client.store_secrets(
        cluster_id, bindings, bobs_secret_salary_object, permissions
    )

    print(f"Bob's secret is stored at {bob_store_id}, and permissions given to Bob")

    ### Instantitate Charlie's client,  store his secret & give permissions and bindings for Alice to compute her program on it
    charlie_user_key = getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_3"))
    charlie_node_key = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_3"))
    charlie_client = create_nillion_client(charlie_user_key, charlie_node_key)
    charlie_user_id = charlie_client.user_id()

    # Charlie creates his secret
    charlies_salary_input = nillion.SecretInteger(10000)
    charlies_secret_salary_object = nillion.Secrets({
        "input3": charlies_salary_input,
    })

    # Bob adds permissions for Alice to compute her program on his secret
    permissions = nillion.Permissions.default_for_user(charlie_user_id)
    permissions.add_compute_permissions({alice_user_id: {program_id}})
    bindings.add_input_party("Party3", charlie_client.party_id())

    print(f"Storing Charlie's secret")
    # Writer stores the permissioned secret, resulting in the secret's store id
    charlie_store_id = await charlie_client.store_secrets(
        cluster_id, bindings, charlies_secret_salary_object, permissions
    )

    print(f"Charlie's secret is stored at {charlie_store_id}, and permissions given to Charlie")

    # Add bindings for the compute
    bindings.add_output_party("Party1", alice_client.party_id())

    print(f"Computing using program {program_id}")
    # do the computation
    compute_id = await alice_client.compute(
        cluster_id,
        bindings,
        [bob_store_id, charlie_store_id],
        nillion.Secrets({"input1": nillion.SecretInteger(1)}),
        nillion.PublicVariables({}),
    )

    print(f"Computation sent to the network, compute_id = {compute_id}")
    print("Waiting computation response")
    while True:
        event = await alice_client.next_compute_event()
        if isinstance(event, nillion.ComputeFinishedEvent):
            print(
                f"Received computation result for {event.uuid}, value = {event.result.value}"
            )
            break


asyncio.run(main())
