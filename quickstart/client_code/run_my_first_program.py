from nada_dsl import *

def nada_main():
    # Define parties
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    party3 = Party(name="Party3")

    # Inputs from Party1
    int1_p1 = SecretInteger(Input(name="int1_p1", party=party1))
    int2_p1 = SecretInteger(Input(name="int2_p1", party=party1))

    # Inputs from Party2
    int1_p2 = SecretInteger(Input(name="int1_p2", party=party2))
    int2_p2 = SecretInteger(Input(name="int2_p2", party=party2))

    # Inputs from Party3
    int1_p3 = SecretInteger(Input(name="int1_p3", party=party3))
    int2_p3 = SecretInteger(Input(name="int2_p3", party=party3))

    # Operations
    sum_p1 = int1_p1 + int2_p1
    diff_p2 = int1_p2 - int2_p2
    prod_p3 = int1_p3 * int2_p3
    combined_sum = sum_p1 + diff_p2 + prod_p3
    avg_combined = combined_sum / Constant(3)  # Assuming we want an average of the combined sum
    complex_calc = (int1_p1 * int1_p2) + (int2_p3 / Constant(2))

    # Outputs
    return [
        Output(sum_p1, "sum_output_p1", party1),
        Output(diff_p2, "diff_output_p2", party2),
        Output(prod_p3, "prod_output_p3", party3),
        Output(combined_sum, "combined_sum_output", party1),
        Output(combined_sum, "combined_sum_output", party2),
        Output(combined_sum, "combined_sum_output", party3),
        Output(avg_combined, "avg_combined_output", party1),
        Output(avg_combined, "avg_combined_output", party2),
        Output(avg_combined, "avg_combined_output", party3),
        Output(complex_calc, "complex_calc_output", party1),
        Output(complex_calc, "complex_calc_output", party2),
        Output(complex_calc, "complex_calc_output", party3)
    ]
