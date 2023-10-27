from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    A = SecretInteger(Input(name="A", party=party1))
    B = SecretInteger(Input(name="B", party=party1))
    C = SecretInteger(Input(name="C", party=party1))
    D = SecretInteger(Input(name="D", party=party1))
    E = SecretInteger(Input(name="E", party=party1))
    F = SecretInteger(Input(name="F", party=party1))
    G = SecretInteger(Input(name="G", party=party1))
    H = SecretInteger(Input(name="H", party=party1))
    I = SecretInteger(Input(name="I", party=party1))

    # A * B * C + D * E + F * G * H + I

    Mul0 = A * B
    Mul1 = Mul0 * C
    Mul2 = D * E
    Add0 = Mul1 + Mul2
    Mul3 = F * G
    Mul4 = Mul3 * H
    Add1 = Add0 + Mul4
    Add2 = Add1 + I

    return [Output(Add2, "my_output", party1)]
