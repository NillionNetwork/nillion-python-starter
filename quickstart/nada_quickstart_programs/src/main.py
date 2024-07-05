from nada_dsl import *

def nada_main():
    # Define parties
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    party3 = Party(name="Party3")

    # Inputs from Party1
    int1_p1 = SecretInteger(Input(name="int1_p1", party=party1))
    weight1_p1 = SecretInteger(Input(name="weight1_p1", party=party1))

    # Inputs from Party2
    int1_p2 = SecretInteger(Input(name="int1_p2", party=party2))
    weight1_p2 = SecretInteger(Input(name="weight1_p2", party=party2))

    # Inputs from Party3
    int1_p3 = SecretInteger(Input(name="int1_p3", party=party3))
    weight1_p3 = SecretInteger(Input(name="weight1_p3", party=party3))

    # Weighted sum calculation
    weighted_sum_p1 = int1_p1 * weight1_p1
    weighted_sum_p2 = int1_p2 * weight1_p2
    weighted_sum_p3 = int1_p3 * weight1_p3
    total_weighted_sum = weighted_sum_p1 + weighted_sum_p2 + weighted_sum_p3

    # Total weight calculation
    total_weight = weight1_p1 + weight1_p2 + weight1_p3

    # Weighted average calculation
    weighted_average = total_weighted_sum / total_weight

    # Outputs
    return [
        Output(weighted_sum_p1, "weighted_sum_output_p1", party1),
        Output(weighted_sum_p2, "weighted_sum_output_p2", party2),
        Output(weighted_sum_p3, "weighted_sum_output_p3", party3),
        Output(total_weighted_sum, "total_weighted_sum_output", party1),
        Output(total_weighted_sum, "total_weighted_sum_output", party2),
        Output(total_weighted_sum, "total_weighted_sum_output", party3),
        Output(total_weight, "total_weight_output", party1),
        Output(total_weight, "total_weight_output", party2),
        Output(total_weight, "total_weight_output", party3),
        Output(weighted_average, "weighted_average_output", party1),
        Output(weighted_average, "weighted_average_output", party2),
        Output(weighted_average, "weighted_average_output", party3)
    ]
