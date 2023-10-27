from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    A = SecretInteger(Input(name="A", party=party1))
    B = PublicInteger(Input(name="B", party=party1))
    C = SecretInteger(Input(name="C", party=party1))
    D = PublicInteger(Input(name="D", party=party1))

    TMP0 = A + B  # secret + public
    TMP1 = C * D  # secret * public
    TMP2 = B + D  # public + public
    TMP3 = B * D  # public * public

    O = TMP0 + TMP1 + TMP2 + TMP3

    return [Output(O, "O", party1)]
