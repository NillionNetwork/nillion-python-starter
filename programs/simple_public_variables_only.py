from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    A = PublicInteger(Input(name="A", party=party1))
    B = PublicInteger(Input(name="B", party=party1))

    O = A * B

    return [Output(O, "O", party1)]
