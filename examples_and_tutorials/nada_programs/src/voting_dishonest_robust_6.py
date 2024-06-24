"""
PROGRAM 6 

nr of voters: m = 3
nr of candidates: n = 2
"""
from nada_dsl import *

def return_val_if_any_false(list_of_bool, val):
    """
    Returns val if any boolean inside list_of_bool is false.

    Parameters:
    - list_of_bool (list of bool): List of boolean values to be checked.
    - val: Value to be returned if any boolean in the list is false.

    Returns:
    - val: If any boolean in the list is false.
    - 0: If none of the booleans in the list are false.
    """
    
    final_value = UnsignedInteger(0)
    for bool in list_of_bool:
        # Use if_else method to check if the current boolean is true,
        # if true, return vfinal_valueal, otherwise return the current val
        final_value = bool.if_else(final_value, val) 

    return final_value

def initialize_voters(nr_voters):
    """
    Initialize voters with unique identifiers.

    Parameters:
    - nr_voters (int): Number of voters.

    Returns:
    - voters (list): List of Party objects representing voters.
    """
    voters = []
    for i in range(nr_voters):
        voters.append(Party(name="Voter" + str(i)))

    return voters

def inputs_initialization(nr_voters, nr_candidates, voters):
    """
    Initialize inputs for votes per candidate.

    Parameters:
    - nr_voters (int): Number of voters.
    - nr_candidates (int): Number of candidates.

    Returns:
    - votes_per_candidate (list): List of lists representing votes per candidate.
    """
    votes_per_candidate = []
    for c in range(nr_candidates):
        votes_per_candidate.append([])
        for v in range(nr_voters):
            votes_per_candidate[c].append(SecretUnsignedInteger(Input(name="v" + str(v) + "_c" + str(c), party=voters[v])))

    return votes_per_candidate

def count_votes(nr_voters, nr_candidates, votes_per_candidate, outparty):
    """
    Count votes for each candidate.

    Parameters:
    - nr_voters (int): Number of voters.
    - nr_candidates (int): Number of candidates.
    - votes_per_candidate (list): List of lists representing votes per candidate.

    Returns:
    - votes (list): List of Output objects representing vote counts for each candidate.
    """
    votes = []
    for c in range(nr_candidates):
        result = votes_per_candidate[c][0]
        for v in range(1, nr_voters):
            result += votes_per_candidate[c][v]
        votes.append(Output(result, "final_vote_count_c" + str(c), outparty))

    return votes

def fn_check_sum(nr_voters, nr_candidates, votes_per_candidate, outparty):
    """
    Check the sum of votes for each voter.

    Parameters:
    - nr_voters (int): Number of voters.
    - nr_candidates (int): Number of candidates.
    - votes_per_candidate (list): List of lists representing votes per candidate.

    Returns:
    - check_sum (list): List of Output objects representing the sum checks for each voter.
    - if_sum_cheat_open (list): List of Output objects representing revealed votes of cheating voters.
    """
    check_sum = []
    if_sum_cheat_open = []
    for v in range(nr_voters):
        check = votes_per_candidate[0][v]
        for c in range(1, nr_candidates):
            vote_v_c = votes_per_candidate[c][v]
            check += vote_v_c
            check_sum.append(Output(check, "check_sum_v" + str(v), outparty))
            # Reveal if cheat
            comp_v_sum = check <= UnsignedInteger(nr_candidates + 1)
            for c in range(nr_candidates):
                vote_v_c = votes_per_candidate[c][v]
                if_sum_cheat_open_v_c = comp_v_sum.if_else(UnsignedInteger(0), vote_v_c)
                if_sum_cheat_open.append(Output(if_sum_cheat_open_v_c, "if_sum_cheat_open_v" + str(v) + "_c" + str(c), outparty))

    return check_sum, if_sum_cheat_open

def fn_check_prod(nr_voters, nr_candidates, votes_per_candidate, outparty):
    """
    Check the product of votes for each voter.

    Parameters:
    - nr_voters (int): Number of voters.
    - nr_candidates (int): Number of candidates.
    - votes_per_candidate (list): List of lists representing votes per candidate.

    Returns:
    - check_prod (list): List of Output objects representing the product checks for each voter.
    - if_prod_cheat_open (list): List of Output objects representing revealed votes of cheating voters.
    """
    check_prod = []
    if_prod_cheat_open = []
    all_comp_prod = []
    for v in range(nr_voters):
        all_comp_v_prod = []
        for c in range(nr_candidates):
            vote_v_c = votes_per_candidate[c][v]
            check_v_c_product = (UnsignedInteger(1) - vote_v_c)*(UnsignedInteger(2) - vote_v_c)
            check_prod.append(Output(check_v_c_product, "check_prod_v" + str(v) + "_c" + str(c), outparty))
            # collect all reveal conditions
            comp_v_c_prod = check_v_c_product < UnsignedInteger(1)
            all_comp_v_prod.append(comp_v_c_prod)
        all_comp_prod.append(all_comp_v_prod)
    # reveal all votes from voter v if 
    for v in range(nr_voters):
        all_comp_v_prod = all_comp_prod[v]
        for c in range(nr_candidates):
            vote_v_c = votes_per_candidate[c][v]
            if_prod_cheat_open_v_c = return_val_if_any_false(all_comp_v_prod, vote_v_c)
            if_prod_cheat_open.append(Output(if_prod_cheat_open_v_c, "if_prod_cheat_open_v" + str(v) + "_c" + str(c), outparty))

    return check_prod, if_prod_cheat_open
				

def nada_main():

    # 0. Compiled-time constants
    nr_voters = 3
    nr_candidates = 2

    # 1. Parties initialization
    voters = initialize_voters(nr_voters)
    outparty = Party(name="OutParty")

	# 2. Inputs initialization
    votes_per_candidate = inputs_initialization(nr_voters, nr_candidates, voters)
    
    # 3. Computation
    # Count the votes
    votes = count_votes(nr_voters, nr_candidates, votes_per_candidate, outparty)
    # Check input soundness
    check_sum, if_sum_cheat_open = fn_check_sum(nr_voters, nr_candidates, votes_per_candidate, outparty)
    check_prod, if_prod_cheat_open = fn_check_prod(nr_voters, nr_candidates, votes_per_candidate, outparty)

    # 4. Output
    # Concatenate lists
    results = votes + check_sum + if_sum_cheat_open + check_prod + if_prod_cheat_open
    return results