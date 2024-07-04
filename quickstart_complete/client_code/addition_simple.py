from nada_dsl import *

def nada_main():
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    
    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    my_int2 = SecretInteger(Input(name="my_int2", party=party1))
    my_int3 = SecretInteger(Input(name="my_int3", party=party2))

    # Add my_int1 and my_int2
    intermediate_result = my_int1 + my_int2
    
    # Add the intermediate result to my_int3 from party2
    final_result = intermediate_result + my_int3


    # Output the final result to both parties
    return [Output(final_result, "final_output_party1", party1),
            Output(final_result, "final_output_party2", party2)]
