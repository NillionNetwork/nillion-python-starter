from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    my_int4 = SecretInteger(Input(name="my_int4", party=party1))  # 102
    my_int2 = SecretInteger(Input(name="my_int2", party=party1))  # 81

    new_int = my_int2 - my_int4  # 81 - 102 = -21

    return [Output(new_int, "my_output", party1)]
