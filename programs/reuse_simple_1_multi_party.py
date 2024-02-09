from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    a = SecretInteger(Input(name="my_int1", party=party1))
    b = SecretInteger(Input(name="my_int2", party=party2))

    result = a * b + a * b

    return [Output(result, "my_output", party1)]
