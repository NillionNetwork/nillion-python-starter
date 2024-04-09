from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    A = SecretInteger(Input(name="A", party=party1))
    B = SecretInteger(Input(name="B", party=party2))
    C = SecretInteger(Input(name="C", party=party1))
    D = SecretInteger(Input(name="D", party=party2))
    E = SecretInteger(Input(name="E", party=party2))
    F = SecretInteger(Input(name="F", party=party2))
    G = SecretInteger(Input(name="G", party=party2))

    result = (
        ((A * B) + C + D) * (E * (F + G))
        + (A * B * (C + D) + E) * F
        + (A + (B * (C + (D * (E + F)))))
    )

    return [Output(result, "my_output", party1)]
