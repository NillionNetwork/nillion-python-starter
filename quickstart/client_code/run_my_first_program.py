from nada_dsl import *

def nada_main():
    # Define two parties
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")

    # Define inputs for Party1
    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    my_int2 = SecretInteger(Input(name="my_int2", party=party1))

    # Define inputs for Party2
    my_int3 = SecretInteger(Input(name="my_int3", party=party2))
    my_int4 = SecretInteger(Input(name="my_int4", party=party2))

    # Perform addition and multiplication
    new_int_add = my_int1 + my_int2
    new_int_mul = my_int3 * my_int4

    # Return the outputs for both parties
    return [
        Output(new_int_add, "addition_output", party1),
        Output(new_int_mul, "multiplication_output", party2)
    ]
