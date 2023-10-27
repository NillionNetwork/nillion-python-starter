from nada_dsl import *


def nada_main():
    @nada_fn
    def add(a: SecretInteger, b: SecretInteger) -> SecretInteger:
        return a + b

    @nada_fn
    def matrix_addition(
        a: Array[SecretInteger], b: Array[SecretInteger]
    ) -> SecretInteger:
        return a.zip(b).map(add).reduce(add)

    party1 = Party(name="Party1")
    party2 = Party(name="Party2")

    my_array_1 = Array(
        Array(SecretInteger(Input(name="my_array_1", party=party1)), size=10), size=10
    )
    my_array_2 = Array(
        Array(SecretInteger(Input(name="my_array_2", party=party2)), size=10), size=10
    )

    output = my_array_1.zip(my_array_2).map(matrix_addition)

    return [Output(output, "output", party1)]
