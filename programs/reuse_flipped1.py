from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    A = SecretInteger(Input(name="A", party=party1))
    B = SecretInteger(Input(name="B", party=party1))
    C = SecretInteger(Input(name="C", party=party1))

    TMP1 = A * B
    TMP2 = C * A
    R = TMP1 + TMP2

    return [Output(R, "R", party1)]
