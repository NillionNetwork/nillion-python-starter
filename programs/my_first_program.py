from nada_dsl import *

def lcm(n1, n2):
    def lcm1(a, b):
        while b != Integer(0):
            a, b = b, a % b
        return a

    return lcm1(n1, n2)

def nada_main():
    party1 = Party(name="Party1")
    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    my_int2 = SecretInteger(Input(name="my_int2", party=party1))

    # Securely compute the LCM using the lcm function
    result = lcm(my_int1, my_int2)

    # Output the result securely
    return [Output(result, "my_output", party1)]
