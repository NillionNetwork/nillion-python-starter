from nada_dsl import *

def nada_main():

    # Define two parties
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")

    # Define secret integers for each party
    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    my_int2 = SecretInteger(Input(name="my_int2", party=party2))

    # Perform operations on the secret integers
    sum_int = my_int1 + my_int2
    product_int = my_int1 * my_int2

    # Return the outputs for each party
    return [
        Output(sum_int, "sum_output", party1),
        Output(product_int, "product_output", party2)
    ]
