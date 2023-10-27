from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    my_rational_1 = SecretRational(Input(name="my_rational_1", party=party1), digits=5)

    return [Output(my_rational_1, "my_output", party1)]
