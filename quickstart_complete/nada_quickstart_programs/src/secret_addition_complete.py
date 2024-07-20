from nada_dsl import *

def nada_main():

    party1 = Party(name="Party1")
    party2 = Party(name="Party2")

    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    my_int2 = SecretInteger(Input(name="my_int2", party=party1))
    my_int3 = SecretInteger(Input(name="my_int3", party=party2))

    sum_int = my_int1 + my_int2
    diff_int = my_int1 - my_int3
    prod_int = my_int2 * my_int3

    max_int = Maximum([sum_int, diff_int, prod_int])

    return [
        Output(sum_int, "sum_output", party1),
        Output(diff_int, "diff_output", party2),
        Output(prod_int, "prod_output", party1),
        Output(max_int, "max_output", party2)
    ]
