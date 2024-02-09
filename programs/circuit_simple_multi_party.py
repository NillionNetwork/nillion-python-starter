from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    my_int2 = SecretInteger(Input(name="my_int2", party=party2))
    my_int3 = SecretInteger(Input(name="my_int3", party=party1))
    my_int4 = SecretInteger(Input(name="my_int4", party=party2))

    new_int1 = my_int1 * my_int2
    new_int2 = my_int3 * my_int4
    new_int3 = new_int1 + new_int2

    return [Output(new_int3, "my_output", party1)]
