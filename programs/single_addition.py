from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    A = SecretInteger(Input(name="A", party=party1))
    B = SecretInteger(Input(name="B", party=party1))

    R = A + B

    return [Output(R, "R", party1)]
