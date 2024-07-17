from nada_dsl import *

def nada_main():
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")

    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    my_int2 = SecretInteger(Input(name="my_int2", party=party1))
    my_int3 = SecretInteger(Input(name="my_int3", party=party2))
    my_int4 = SecretInteger(Input(name="my_int4", party=party2))

    sum_ints = my_int1 + my_int2 + my_int3 + my_int4
    product_ints = my_int1 * my_int2 * my_int3 * my_int4
    average_ints = sum_ints / SecretInteger(value=4, party=party1)

    comparison_result = my_int1 > my_int3
    conditional_result = If(comparison_result, my_int1 - my_int3, my_int3 - my_int1)

    return [
        Output(sum_ints, "sum_output", party1),
        Output(product_ints, "product_output", party1),
        Output(average_ints, "average_output", party2),
        Output(conditional_result, "conditional_output", party2)
    ]

if __name__ == "__main__":
    nada_main()
