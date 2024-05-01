##########################################################################################

#                                   VOTING  --  PART 3

##########################################################################################

import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
from dotenv import load_dotenv
from config import (
    CONFIG,
    CONFIG_CANDIDATES,
    CONFIG_PARTY_1,
    CONFIG_N_PARTIES
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile
from digest_result import digest_plurality_vote_honest_result, digest_plurality_vote_dishonest_with_abort_result, digest_plurality_vote_robust_result


load_dotenv()

parser = argparse.ArgumentParser(
    description="Create a secret on the Nillion network with set read/retrieve permissions"
)

parser.add_argument(
    "--program_id",
    required=True,
    type=str,
    help="Program ID of the voting program",
)

parser.add_argument(
    "--party_ids_to_store_ids",
    required=True,
    nargs='+',
    type=str,
    help="List of partyid:storeid pairs of the secrets, with each pair separated by a space",
)

args = parser.parse_args()

async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")

    #####################################
    # 1. Parties initialization         #
    #####################################

    #############################
    # 1.1 Owner initialization  #
    #############################
    # Alice initializes a client
    client_alice = create_nillion_client(
        getUserKeyFromFile(CONFIG_PARTY_1["userkey_file"]), 
        getNodeKeyFromFile(CONFIG_PARTY_1["nodekey_file"])
    )
    party_id_alice = client_alice.party_id

    #####################################
    # 4. Storing votes                  #
    #####################################
    # Add any computation time secrets
    # Alice provides her vote at compute time

    party_name_alice = CONFIG_PARTY_1["party_name"]
    secret_votes = CONFIG_PARTY_1["secret_votes"]
    secret_votes = {key: nillion.SecretUnsignedInteger(value) for key, value in secret_votes.items()}
    compute_time_secrets = nillion.Secrets(secret_votes)

    print(f"\n🎉 {party_name_alice} provided her vote as a compute time secret.")

    #####################################
    # 6. Owner execute computation      #
    #####################################
    # Create computation bindings for voting program
    compute_bindings = nillion.ProgramBindings(args.program_id)

    #################################################
    # 6.1 Bind voter to input party in the program  #
    #################################################
    # Add Alice as an input party
    compute_bindings.add_input_party(CONFIG_PARTY_1["party_role"], party_id_alice)

    # Also add Bob and Charlie as input parties
    party_ids_to_store_ids = {}
    i=0
    for pair in args.party_ids_to_store_ids:
        party_id, store_id = pair.split(':')
        party_role = CONFIG_N_PARTIES[i]['party_role']
        compute_bindings.add_input_party(party_role, party_id)
        party_ids_to_store_ids[party_id] = store_id
        i=i+1

    ##################################################
    # 6.2 Bind owner to output party in the program  #
    ##################################################
    # Add an output party (Alice). 
    # The output party reads the result of the blind computation
    compute_bindings.add_output_party("OutParty", party_id_alice)

    print(f"Computing using program {args.program_id}")

    # Compute on the secret with all store ids. Note that there are no compute time secrets or public variables
    compute_id = await client_alice.compute(
        cluster_id,
        compute_bindings,
        list(party_ids_to_store_ids.values()), # Bob and Charlie's stored secrets
        compute_time_secrets, # Alice's computation time secret
        nillion.PublicVariables({}),
    )

    # Print compute result
    print(f"The computation was sent to the network. compute_id: {compute_id}")
    print("Waiting computation response...")
    while True:
        compute_event = await client_alice.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            dict_result = compute_event.result.value
            print(f"🖥️  The output result is {dict_result}\n")

            # Digest the result
            program_name = os.path.basename(args.program_id)
            nr_candidates = CONFIG["nr_candidates"]
            nr_voters = CONFIG["nr_voters"]
            voters = CONFIG_N_PARTIES
            voters.insert(0, CONFIG_PARTY_1)
            candidates = CONFIG_CANDIDATES
            if program_name == "voting_dishonest_robust_6":
                print("Let use digest the result given by the network:")
                winner, total_votes, cheaters = digest_plurality_vote_robust_result(dict_result, nr_candidates, nr_voters)
                winner_name = candidates[winner]
                cheaters_names = [voters[voter]["party_name"] for voter in cheaters]
                print(f"🏆 Winner is {winner_name}")
                print(f"🔢 Total number of votes per candidate:")
                print(f"          Dave: {total_votes[0]}")
                print(f"          Emma: {total_votes[1]}")
                print(f"🕵️‍♂️ List of cheaters: {cheaters_names}")
            elif program_name in ["voting_honest_1", "voting_honest_2"]:
                digest_plurality_vote_honest_result(dict_result, nr_candidates, nr_voters)
            elif program_name == "voting_dishonest_abort_5":
                digest_plurality_vote_dishonest_with_abort_result(dict_result, nr_candidates, nr_voters)
            
            break
    
asyncio.run(main())
