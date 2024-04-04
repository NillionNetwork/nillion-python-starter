"""
PROGRAM 2

nr of voters: m = 5
nr of candidates: n = 3
"""
from nada_dsl import *

def nada_main():
    
    # 0. Compiled-time constants
    nr_voters = 3
    nr_candidates = 2

    # 1. Parties initialization
    voters = []
    for i in range(nr_voters):
        voters.append(Party(name="Voter" + str(i)))
    outparty = Party(name="OutParty")

    # 2. Inputs initialization
    votes_per_candidate = []
    for c in range(nr_candidates):
        votes_per_candidate.append([])
        for v in range(nr_voters):
            votes_per_candidate[c].append(SecretUnsignedInteger(Input(name="v" + str(v) + "_c" + str(c), party=voters[v])))

    # 3. Computation
    results = []
    for c in range(nr_candidates):
        result = votes_per_candidate[c][0]
        for v in range(1, nr_voters):
            ## Add votes for candidate c
            result += votes_per_candidate[c][v]
        # 4. Output
        results.append(Output(result, "final_vote_count_c" + str(c), outparty))

    return results