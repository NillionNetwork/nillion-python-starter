from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    my_rational_1 = SecretRational(Input(name="my_rational_1", party=party1), digits=4)
    my_rational_2 = SecretRational(Input(name="my_rational_2", party=party1), digits=5)

    result = my_rational_1 * my_rational_2

    return [Output(result, "my_output", party1)]
