from nada_dsl import *


def nada_main():
    party1 = Party(name="Party1")
    a = SecretInteger(Input(name="a", party=party1))
    b = SecretInteger(Input(name="b", party=party1))
    c = SecretInteger(Input(name="c", party=party1))
    d = SecretInteger(Input(name="d", party=party1))

    my_tuple_1 = Tuple.new(a, b)
    my_tuple_2 = Tuple.new(c, d)
    my_array_1 = Array.new(my_tuple_1, my_tuple_2)
    result = unzip(my_array_1)
    
    return [Output(result, "my_output", party1)]
