from nada_dsl import *

def nada_main():
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    party3 = Party(name="Party3")
    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    my_int2 = SecretInteger(Input(name="my_int2", party=party2))
    my_int3 = SecretInteger(Input(name="my_int3", party=party3))

    new_int = my_int1 + my_int2 + my_int3

    return [Output(new_int, "my_output", party1)]
