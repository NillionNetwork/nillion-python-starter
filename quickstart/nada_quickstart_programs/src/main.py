from nada_dsl import *
from math import gcd 

def nada_main():
    party1 = Party(name="Party1")

    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    my_int2 = SecretInteger(Input(name="my_int2", party=party1))

    sum_int = my_int1 + my_int2

    difference_int = my_int1 - my_int2

    product_int = my_int1 * my_int2

    quotient_int = my_int1 // my_int2

    gcd_int = gcd(my_int1, my_int2)

    is_multiple = (my_int1 % my_int2) == 0
    multiple_message = is_multiple.if_else("Yes", "No")

    return [
        Output(sum_int, "sum_output", party=party1),
        Output(difference_int, "difference_output", party=party1),
        Output(product_int, "product_output", party=party1),
        Output(quotient_int, "quotient_output", party=party1),
        Output(gcd_int, "gcd_output", party=party1),
        Output(multiple_message, "multiple_output", party=party1)
    ]
