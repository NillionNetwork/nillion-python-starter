from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    my_int1 = SecretInteger(Input(name="my_int1", party=party1))  # 102
    my_int2 = SecretInteger(Input(name="my_int2", party=party2))  # 81

    new_int = my_int2 - my_int1  # 81 - 102 = -21

    return [Output(new_int, "my_output", party1)]
