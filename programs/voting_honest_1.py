"""
PROGRAM 1

nr of voters: m = 3
nr of candidates: n = 2
"""
from nada_dsl import *

def nada_main():

	# 1. Parties initialization
    voter0 = Party(name="Voter0")
    voter1 = Party(name="Voter1")
    voter2 = Party(name="Voter2")
    outparty = Party(name="OutParty") 

	# 2. Inputs initialization
    ## Votes from voter 0
    v0_c0 = SecretUnsignedInteger(Input(name="v0_c0", party=voter0))
    v0_c1 = SecretUnsignedInteger(Input(name="v0_c1", party=voter0))
    ## Votes from voter 1
    v1_c0 = SecretUnsignedInteger(Input(name="v1_c0", party=voter1))
    v1_c1 = SecretUnsignedInteger(Input(name="v1_c1", party=voter1))
    ## Votes from voter 2
    v2_c0 = SecretUnsignedInteger(Input(name="v2_c0", party=voter2))
    v2_c1 = SecretUnsignedInteger(Input(name="v2_c1", party=voter2))

	# 3. Computation
    ## Add votes for candidate 0
    result_c0 = v0_c0 + v1_c0 + v2_c0
    ## Add votes for candidate 1
    result_c1 = v0_c1 + v1_c1 + v2_c1
    
    # 4. Output
    result_c0 = Output(result_c0, "final_vote_count_c0", outparty)
    result_c1 = Output(result_c1, "final_vote_count_c1", outparty)

    return [result_c0, result_c1]