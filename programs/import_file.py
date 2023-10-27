from nada_dsl import *
from lib.library import add


def nada_main():
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    my_int2 = SecretInteger(Input(name="my_int2", party=party2))

    new_int1 = add(my_int1, my_int2)

    return [Output(new_int1, "my_output", party1)]
