from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    my_array_1 = Array(SecretInteger(Input(name="my_array_1", party=party1)), size=10)
    my_int = SecretInteger(Input(name="my_int", party=party1))

    @nada_fn
    def inc(a: SecretInteger) -> SecretInteger:
        return a + my_int

    new_array = my_array_1.map(inc)

    out = Output(new_array, "out", party1)

    return [out]
