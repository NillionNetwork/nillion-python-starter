from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    my_integer_array = Array(SecretInteger(Input(name="my_integer_array", party=party1)), size=5)
    return [Output(my_integer_array, "my_output", party1)]
