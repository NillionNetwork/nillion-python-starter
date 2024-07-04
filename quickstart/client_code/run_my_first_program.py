from nada_dsl import *

def nada_main():
    # Define two parties
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    
    # Define secret integers for each party
    secret1_p1 = SecretInteger(Input(name="secret1_p1", party=party1))
    secret2_p1 = SecretInteger(Input(name="secret2_p1", party=party1))
    
    secret1_p2 = SecretInteger(Input(name="secret1_p2", party=party2))
    secret2_p2 = SecretInteger(Input(name="secret2_p2", party=party2))
    
    # Perform arithmetic operations
    sum_p1 = secret1_p1 + secret2_p1
    sum_p2 = secret1_p2 + secret2_p2
    
    product_p1 = secret1_p1 * secret2_p1
    product_p2 = secret1_p2 * secret2_p2

    combined_sum = sum_p1 + sum_p2
    combined_product = product_p1 * product_p2
    
    # Debugging outputs
    print(f"Sum Party 1: {sum_p1}")
    print(f"Sum Party 2: {sum_p2}")
    print(f"Product Party 1: {product_p1}")
    print(f"Product Party 2: {product_p2}")
    print(f"Combined Sum: {combined_sum}")
    print(f"Combined Product: {combined_product}")
    
    # Returning outputs for both parties
    return [
        Output(sum_p1, "sum_output_p1", party1),
        Output(sum_p2, "sum_output_p2", party2),
        Output(product_p1, "product_output_p1", party1),
        Output(product_p2, "product_output_p2", party2),
        Output(combined_sum, "combined_sum_output", party1),
        Output(combined_product, "combined_product_output", party2)
    ]

# Create the NaDa program
nada_program = nada_main()
