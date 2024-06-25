from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    my_int2 = SecretInteger(Input(name="my_int2", party=party1))

    #A voting logic in nada, the result will be 1 if my_int1 has the majority

    total_votes = my_int1 + my_int2
    cutoff = total_votes // 2

    majority = my_int1 > cutoff

    result = majority.if_else(1, 0)


    return [Output(result, "voting_result", party1)]