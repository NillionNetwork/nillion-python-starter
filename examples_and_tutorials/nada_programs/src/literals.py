from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    A = SecretInteger(Input(name="A", party=party1))
    C = SecretInteger(Input(name="C", party=party1))

    TMP0 = A * Integer(13) + Integer(13)    # secret * literal + literal (checks literal re-use)
    TMP1 = C * Integer(50)                  # secret * literal
    TMP2 = Integer(13) + Integer(50)        # literal + literal
    TMP3 = Integer(13) * Integer(50)        # literal * literal

    O = TMP0 + TMP1 + TMP2 + TMP3

    return [Output(O, "O", party1)]
