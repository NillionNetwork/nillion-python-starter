from nada_dsl import *

def nada_main():
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    party3 = Party(name="Party3")

    input1 = SecretInteger(Input(name="input1", party=party1))
    input2 = SecretInteger(Input(name="input2", party=party2))
    input3 = SecretInteger(Input(name="input3", party=party3))

    largest_position = (
        (input1 > input2).if_else(
            (input1 > input3).if_else(Integer(1), Integer(3)),
            (input2 > input3).if_else(Integer(2), Integer(3))
        )
    )

    out = Output(largest_position, "largest_position", party1)

    return [out]