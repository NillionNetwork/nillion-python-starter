from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    my_array_1 = Array(SecretInteger(Input(name="my_array_1", party=party1)), size=10)
    my_array_2 = Array(SecretInteger(Input(name="my_array_2", party=party2)), size=10)

    unzipped = unzip(my_array_2.zip(my_array_1))

    @nada_fn
    def add(a: SecretInteger, b: SecretInteger) -> SecretInteger:
        return a + b

    new_array = my_array_1.zip(my_array_2).map(add).reduce(add, my_int1)

    out1 = Output(unzipped, "zip.unzip.tuple", party1)
    out2 = Output(new_array, "zip.map.reduce.array", party1)

    return [out1, out2]
