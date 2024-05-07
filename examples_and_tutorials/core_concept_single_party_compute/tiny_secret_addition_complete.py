import asyncio
import py_nillion_client as nillion
import os
import sys
import pytest

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()

# This python script stores the tiny_secret_addition_complete program in the network, store secrets, and compute
async def main():
    # 0. The bootstrap-local-environment.sh script put nillion-devnet config variables into the .env file
    # Get cluster_id, user_key, and node_key from the .env file
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    userkey = getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    nodekey = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_1"))

    # ✅ 1. Initialize NillionClient against nillion-devnet
    # Create Nillion Client for user
    client = create_nillion_client(userkey, nodekey)

    # ✅ 2. Get the user id and party id from NillionClient
    party_id = client.party_id
    user_id = client.user_id

    # ✅ 3. Store a compiled Nada program in the network
    # Set the program name
    program_name="tiny_secret_addition_complete"
    # Set the path to the compiled program
    program_mir_path=f"../../programs-compiled/{program_name}.nada.bin"
    # Store the program
    action_id = await client.store_program(
        cluster_id, program_name, program_mir_path
    )
    # Create a variable for the program_id, which is the {user_id}/{program_name}
    program_id=f"{user_id}/{program_name}"
    print('Stored program. action_id:', action_id)
    print('Stored program_id:', program_id)


    # ✅ 4. Create the 1st secret with bindings to the program
    # Create a secret named "my_int1" with any value, ex: 500
    new_secret = nillion.Secrets({
        "my_int1": nillion.SecretInteger(500),
    })

    # Create secret bindings object to bind the secret to the program and set the input party
    secret_bindings = nillion.ProgramBindings(program_id)

    # Set the input party for the secret
    # The party name needs to match the party name that is storing "my_int1" in the program
    party_name="Party1"
    secret_bindings.add_input_party(party_name, party_id)

    # ✅ 5. Store the secret in the network and print the returned store_id
    store_id = await client.store_secrets(
        cluster_id, secret_bindings, new_secret, None
    )
    print(f"Computing using program {program_id}")
    print(f"Use secret store_id: {store_id}")

    # ✅ 6. Create compute bindings to set input and output parties
    compute_bindings = nillion.ProgramBindings(program_id)
    compute_bindings.add_input_party(party_name, party_id)
    compute_bindings.add_output_party(party_name, party_id)

    # ✅ 7. Compute on the program with 1st secret from the network, and the 2nd secret, provided at compute time

    # Add my_int2, the 2nd secret at computation time
    computation_time_secrets = nillion.Secrets({"my_int2": nillion.SecretInteger(10)})
    
    # Compute on the secret
    compute_id = await client.compute(
        cluster_id,
        compute_bindings,
        [store_id],
        computation_time_secrets,
        nillion.PublicVariables({}),
    )

    # ✅ 8. Print the computation result
    print(f"The computation was sent to the network. compute_id: {compute_id}")
    while True:
        compute_event = await client.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            print(f"🖥️  The result is {compute_event.result.value}")
            return compute_event.result.value
    
if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    result = await main()
    assert result == {'my_output': 510}
