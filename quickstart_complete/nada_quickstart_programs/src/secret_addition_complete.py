from nada_dsl import *

def nada_main():
    # Define three parties
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    party3 = Party(name="Party3")

    # Define secret integers for each party
    my_int1_party1 = SecretInteger(Input(name="my_int1_party1", party=party1))
    my_int2_party1 = SecretInteger(Input(name="my_int2_party1", party=party1))
    my_int3_party1 = SecretInteger(Input(name="my_int3_party1", party=party1))

    my_int1_party2 = SecretInteger(Input(name="my_int1_party2", party=party2))
    my_int2_party2 = SecretInteger(Input(name="my_int2_party2", party=party2))
    my_int3_party2 = SecretInteger(Input(name="my_int3_party2", party=party2))

    my_int1_party3 = SecretInteger(Input(name="my_int1_party3", party=party3))
    my_int2_party3 = SecretInteger(Input(name="my_int2_party3", party=party3))
    my_int3_party3 = SecretInteger(Input(name="my_int3_party3", party=party3))

    # Perform complex operation involving all parties
    intermediate_result1 = my_int1_party1 * my_int2_party2
    intermediate_result2 = my_int2_party1 + my_int3_party2
    intermediate_result3 = my_int3_party1 - my_int1_party2

    final_result_party1 = intermediate_result1 + intermediate_result2
    final_result_party2 = intermediate_result2 * intermediate_result3
    final_result_party3 = intermediate_result3 + intermediate_result1

    # Define outputs for each party
    outputs = [
        Output(final_result_party1, "output_party1", party1),
        Output(final_result_party2, "output_party2", party2),
        Output(final_result_party3, "output_party3", party3)
    ]

    return outputs
