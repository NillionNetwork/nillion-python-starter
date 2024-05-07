from pdb import set_trace as bp
import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
from dotenv import load_dotenv
import random
from math import sqrt
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile

load_dotenv()

# 1 Party running simple addition on 1 stored secret and 1 compute time secret
async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    userkey = getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    nodekey = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_1"))
    client = create_nillion_client(userkey, nodekey)
    party_id = client.party_id
    user_id = client.user_id
    party_0_name="Party0"
    party_1_name="Party1"
    out_party_name="OutParty"
    program_name="correlation_coefficient"
    program_mir_path=f"../../programs-compiled/{program_name}.nada.bin"

    # store program
    action_id = await client.store_program(
        cluster_id, program_name, program_mir_path
    )

    program_id=f"{user_id}/{program_name}"
    print('Stored program. action_id:', action_id)
    print('Stored program_id:', program_id)
    
    # Config elements
    linear = lambda x: 30*x + 21
    p0_points = 10
    p1_points = 10
    precision = 5

    random.seed(42)

    # Create inputs for both parties
    party_0_dict = {}
    for i in range(p0_points):
        party_0_dict[f"x{i}"] = nillion.SecretInteger(i+1)
        party_0_dict[f"y{i}"] = nillion.SecretInteger(linear(i+1) + random.randint(0, 10))

    party_1_dict = {}
    for i in range(p0_points, p0_points + p1_points):
        party_1_dict[f"x{i}"] = nillion.SecretInteger(i+1)
        party_1_dict[f"y{i}"] = nillion.SecretInteger(linear(i+1) + random.randint(0, 10))


    # Parties store the secrets
    party_0_secrets = nillion.Secrets(party_0_dict)
    party_1_secrets = nillion.Secrets(party_1_dict)

    # Bind to the corresponding pary in the program
    secret_bindings = nillion.ProgramBindings(program_id)
    secret_bindings.add_input_party(party_0_name, party_id)
    secret_bindings.add_input_party(party_1_name, party_id)

    # Give core_concept_permissions to owner to compute with my vote
    secret_permissions = nillion.Permissions.default_for_user(user_id)
    secret_permissions.add_compute_permissions({
        user_id: {program_id},
    })

    store_ids = []
    # Store in the network
    print(f"Storing party 0: {party_0_secrets}")
    store_id = await client.store_secrets(
        cluster_id, secret_bindings, party_0_secrets, secret_permissions
    )
    store_ids.append(store_id)
    print(f"Stored party 0 with store_id ={store_id}")


    print(f"Storing party 1: {party_1_secrets}")
    store_id = await client.store_secrets(
        cluster_id, secret_bindings, party_1_secrets, secret_permissions
    )
    store_ids.append(store_id)
    print(f"Stored party 1 with store_id ={store_id}")

    # Bind the parties in the computation to the client to set input and output parties
    compute_bindings = nillion.ProgramBindings(program_id)
    compute_bindings.add_input_party(party_0_name, party_id)
    compute_bindings.add_input_party(party_1_name, party_id)
    compute_bindings.add_output_party(out_party_name, party_id)
    computation_time_secrets = nillion.Secrets({})

    print(f"Computing using program {program_id}")
    print(f"Use secret store_id: {store_id}")
    
    # Compute on the secret
    compute_id = await client.compute(
        cluster_id,
        compute_bindings,
        store_ids,
        computation_time_secrets,
        nillion.PublicVariables({}),
    )

    # Print compute result
    print(f"The computation was sent to the network. compute_id: {compute_id}")
    while True:
        compute_event = await client.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            print(f"🖥️  The result is {compute_event.result.value}")
            corr_coeff_squared = compute_event.result.value["correlation_coefficient_squared"] / 10**precision
            sign = 1 if compute_event.result.value["sign"] else -1
            corr_coeff = round(sign * sqrt(corr_coeff_squared), precision)
            print(f"📈  Correlation coefficient = {corr_coeff} with precision {precision}.")
            return compute_event.result.value


if __name__ == "__main__":
    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    result = await main()
    assert result == {'correlation_coefficient_squared': 99958, 'sign': 1}