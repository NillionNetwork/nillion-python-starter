from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    A = SecretInteger(Input(name="A", party=party2))
    B = SecretInteger(Input(name="B", party=party2))

    R = A + B

    return [Output(R, "R", party1)]
