##########################################################################################

#                                   SINGLE FILE VOTING

##########################################################################################


import asyncio
import py_nillion_client as nillion
import os
import sys
from dotenv import load_dotenv
from config import (
    CONFIG
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromFile
from digest_result import digest_plurality_vote_honest_result, digest_plurality_vote_dishonest_with_abort_result, digest_plurality_vote_robust_result

load_dotenv()

async def main():

    cluster_id = os.getenv("NILLION_CLUSTER_ID")

    while True:

        # Below, you can choose which voting program to use. In case you choose a voting program 
        # different from the robust version ('voting_dishonest_robust_6'), you can complete  
        # either 'digest_plurality_vote_honest_result()' or 'digest_plurality_vote_dishonest_with_abort_result()' 
        # functions above to digest the result.
        #
        # Existing voting programs:
        #
        # program_name = "voting_honest_1"  
        # program_name = "voting_honest_2"  
        # program_name = "voting_dishonest_abort_5"      
        # program_name = "voting_dishonest_robust_6"

        print("Choose a program to test:")
        print("1. voting_honest_1")
        print("2. voting_honest_2")
        print("3. voting_dishonest_abort_5")
        print("4. voting_dishonest_robust_6")

        choice = input("Enter the number corresponding to your choice: ")

        programs = {
            "1": "voting_honest_1",
            "2": "voting_honest_2",
            "3": "voting_dishonest_abort_5",
            "4": "voting_dishonest_robust_6"
        }

        if choice in programs:
            program_name = programs[choice]
            print("You have chosen:", program_name)
            print(" _         _   _                  _                  _ _   _     ")
            print("| |    ___| |_( )___  __   _____ | |_ ___  __      _(_) |_| |__  ")
            print("| |   / _ \\ __|// __| \\ \\ / / _ \\| __/ _ \\ \\ \\ /\\ / / | __| '_ \\ ")
            print("| |__|  __/ |_  \\__ \\  \\ V / (_) | ||  __/  \\ V  V /| | |_| | | |")
            print("|_____\\___|\\__| |___/   \\_/_\\___/ \\__\\___|   \\_/\\_/ |_|\\__|_| |_|")
            print("                    _____(_) | (_) ___  _____| |                 ")
            print("                   |  _  | | | | |/ _ \\|  _  | |                 ")
            print("                   | | | | | | | | (_) | | | |_|                 ")
            print("                   |_| |_|_|_|_|_|\\___/|_| |_(_)                 ")
            print("                                                                 ")
            break  # Exit the loop if a valid choice is made
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
   
    # We initialize one party 'general_client' that represents all different parties. 
    #
    # In a real environment, the clients must run in different machines with 
    # different node and user keys. 
    # 
    # The script has the following flow:
    #     1. Parties initialization
    #     2. Owner stores a program.
    #     3. (Real environment:) Owner sends the program ID to all voters.
    #     4. Voters store votes:
    #         4.1 Bind voter to party in the program
    #         4.2 Set compute permission to owner
    #     5. (Real environment:) Voters send their their party IDs and store IDs to the owner.
    #     6. Owner compute voting system using votes from voters.
    
    nr_candidates = CONFIG["nr_candidates"]
    nr_voters = CONFIG["nr_voters"]

    #####################################
    # 1. Parties initialization         #
    #####################################

    ######################################
    # 1.0 General client initialization  #
    ######################################
    userkey = getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    nodekey = getNodeKeyFromFile(os.getenv("NILLION_NODEKEY_PATH_PARTY_1"))
    general_client = create_nillion_client(userkey, nodekey)

    # #############################
    # # 1.1 Owner initialization  #
    # #############################
    # # Path to the user and node key generated in previous step
    # owner_nodekey_path = "/path/to/owner_node.key"
    # owner_nodekey = nillion.NodeKey.from_file(owner_nodekey_path)
    # owner_userkey_path = "/path/to/owner_user.key"
    # owner_userkey = nillion.UserKey.from_file(owner_userkey_path)
    # owner = nillion.NillionClient(
    #     owner_nodekey,
    #     bootnodes,
    #     nillion.ConnectionMode.relay(),
    #     owner_userkey,
    #     payments_config=payments_config
    # )

    # #############################
    # # 1.2 Voters initialization #
    # #############################
    # # Initialize voters
    # voters = []
    # for v in range(nr_voters):
    #     # Path to the user and node key generated in previous step
    #     voter_nodekey_path = "/path/to/voter"+str(v)+"_node.key"
    #     voter_nodekey = nillion.NodeKey.from_file(voter_nodekey_path)
    #     voter_userkey_path = "/path/to/voter"+str(v)+"_user.key"
    #     voter_userkey = nillion.UserKey.from_file(voter_userkey_path)
    #     voter = nillion.NillionClient(
    #         voter_nodekey,
    #         bootnodes,
    #         nillion.ConnectionMode.relay(),
    #         voter_userkey,
    #         payments_config=payments_config
    #     )
    #     voters.append(voter)


    #####################################
    # 2. Storing program                #
    #####################################
    
    # Note: do not forget to compile the programs and store the corresponding .nada.bin file.
    program_mir_path = f"../../programs-compiled/{program_name}.nada.bin"
    if os.path.exists(program_mir_path):
        None
    else:
        raise FileNotFoundError(f"The file '{program_mir_path}' does not exist.\nMake sure you compiled the PyNada programs with './compile_programs.sh'.\nCheck README.md for more details.")

    # Store program in the Network
    print(f"Storing program in the network: {program_name}")
    # action_id = await owner.store_program(
    action_id = await general_client.store_program(
        cluster_id, program_name, program_mir_path
    )
    print("action_id is: ", action_id)
    # program_id = owner.user_id + "/" + program_name
    program_id = general_client.user_id + "/" + program_name
    print("program_id is: ", program_id)

    #####################################
    # 3. Send program ID                #
    #####################################

    # This requires its own mechanism in a real environment. 
    # In this demo, we just reuse the variable 'program_id'.

    #####################################
    # 4. Storing votes                  #
    #####################################

    # Each voter stores its vote. In this demo, we assume each voter has a file
    # containing their votes for each candidate. E.g. voter 0 has a file 'inputs/v0_input.txt'
    # with the following format:
    #  ==============
    #  1
    #  2
    #  ==============
    #  This means, voter 0 assigns 1 to candidate 0 and 2 to candidate 1.

    # Voters store the secrets
    store_ids = []
    for v in range(nr_voters):
        voter_v = general_client
        # voter_v = voters[v]
        print("voter_v: ", voter_v)
        # structure v's votes
        v_vote_dic = {}
        v_input_file = "inputs/v"+str(v)+"_input.txt"
        with open(v_input_file, 'r') as file:
            c = 0
            for line in file:
                # Remove leading and trailing whitespaces, then convert to integer
                v_c_vote_value = int(line.strip())
                v_c_vote = nillion.SecretUnsignedInteger(v_c_vote_value)
                v_vote_dic["v"+str(v)+"_c"+str(c)] = v_c_vote
                c += 1
        v_to_be_store_secrets = nillion.Secrets(v_vote_dic)
        
        ###########################################
        # 4.1 Bind voter to party in the program  #
        ###########################################
        v_bindings = nillion.ProgramBindings(program_id)
        v_bindings.add_input_party("Voter"+str(v), voter_v.party_id)

        ###########################################
        # 4.2 Set compute permissions to owner    #
        ###########################################
        # Give permissions to owner to compute with my vote
        v_permissions = nillion.Permissions.default_for_user(voter_v.user_id)
        v_permissions.add_compute_permissions({
            # owner.user_id: {program_id},
            general_client.user_id: {program_id},
        })

        # Store in the network
        print("Storing vote by voter "+str(v)+f": {v_to_be_store_secrets}")
        store_id = await voter_v.store_secrets(
            cluster_id, v_bindings, v_to_be_store_secrets, v_permissions
        )
        store_ids.append(store_id)
        print(f"Stored vote by voter "+str(v)+f" with store_id ={store_id}")

    #####################################
    # 5. Send party IDs and store IDs   #
    #####################################

    # This requires its own mechanism in a real environment. 
    # In this demo, we just reuse the variable 'store_ids' and
    # the voters' clients to extra their party IDs.
        
    #####################################
    # 6. Owner execute computation      #
    #####################################

    #################################################
    # 6.1 Bind voter to input party in the program  #
    #################################################
    owner_bindings = nillion.ProgramBindings(program_id)
    for v in range(nr_voters):
        # owner_bindings_0.add_input_party("Voter"+str(v), voters[v].party_id)
        owner_bindings.add_input_party("Voter"+str(v), general_client.party_id)

    ##################################################
    # 6.2 Bind owner to output party in the program  #
    ##################################################
    # Bind the "OutParty" party in the computation to the owner's client
    # owner_bindings.add_output_party("OutParty", owner.party_id)
    owner_bindings.add_output_party("OutParty", general_client.party_id)
    
    # No secret is directly passed to 'compute'. It only uses
    # stored secrets.
    to_be_used_in_computation = nillion.Secrets({})

    print(f"Computing using program {program_id}")
    print(f"Stored secrets: {store_ids}")
    print(f"Provided secret: {to_be_used_in_computation}")
    
    # Owner can execute the computation
    # compute_id = await owner.compute(
    compute_id = await general_client.compute(
        cluster_id,
        owner_bindings,
        store_ids,
        to_be_used_in_computation,
        nillion.PublicVariables({}),
    )

    print(f"Computation sent to the network, compute_id = {compute_id}")
    print("Waiting computation response...")
    while True:
        compute_event = await general_client.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            dict_result = compute_event.result.value
            print(f"🖥️  The result is: {dict_result}\n")

            if program_name == "voting_dishonest_robust_6":
                print("Let use digest the result given by the network:")
                winner, total_votes, cheaters = digest_plurality_vote_robust_result(dict_result, nr_candidates, nr_voters)
                print(f"🏆 Winner is candidate with ID={winner}")
                print(f"🔢 Total number of votes per candidate: {total_votes}")
                print(f"🕵️‍♂️ List of cheaters' IDs: {cheaters}")
            elif program_name in ["voting_honest_1", "voting_honest_2"]:
                digest_plurality_vote_honest_result(dict_result, nr_candidates, nr_voters)
            elif program_name == "voting_dishonest_abort_5":
                digest_plurality_vote_dishonest_with_abort_result(dict_result, nr_candidates, nr_voters)
            
            break
    
 

asyncio.run(main())