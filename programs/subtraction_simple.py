from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    my_int1 = SecretInteger(Input(name="my_int1", party=party1))  # 32
    my_int2 = SecretInteger(Input(name="my_int2", party=party1))  # 81

    new_int = my_int2 - my_int1

    return [Output(new_int, "my_output", party1)]
