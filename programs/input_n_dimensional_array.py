from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    a = Array(Array(Array(SecretInteger(Input(name="a", party=party1)), size=5), size=5), size=5)
    return [Output(a, "my_output", party1)]
