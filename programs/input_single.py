from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    x = my_int1
    y = x
    z = y
    return [Output(z, "my_output", party1)]
