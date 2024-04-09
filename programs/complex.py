from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    A = SecretInteger(Input(name="A", party=party1))
    B = SecretInteger(Input(name="B", party=party1))
    C = SecretInteger(Input(name="C", party=party1))
    D = SecretInteger(Input(name="D", party=party1))
    E = SecretInteger(Input(name="E", party=party1))
    F = SecretInteger(Input(name="F", party=party1))

    TMP1 = A * B
    PRODUCT1 = TMP1 * C
    TMP2 = C * D
    PRODUCT2 = TMP2 * E
    PRODUCT3 = E * F
    PARTIAL = PRODUCT1 + PRODUCT2
    FINAL = PARTIAL + PRODUCT3

    return [Output(FINAL, "FINAL", party1)]
