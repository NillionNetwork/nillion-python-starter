from nada_dsl import Array, Party, SecretInteger, Output, Input, nada_fn


def nada_main():
    party1 = Party(name="Party1")
    my_array_1 = Array(SecretInteger(Input(name="my_array_1", party=party1)), size=4)
    my_int1 = SecretInteger(Input(name="my_int1", party=party1))

    @nada_fn
    def add(a: SecretInteger, b: SecretInteger) -> SecretInteger:
        return a + b

    addition = my_array_1.reduce(add, my_int1)

    out2 = Output(addition, "reduce.addition", party1)

    return [out2]
