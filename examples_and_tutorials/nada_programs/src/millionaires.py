from nada_dsl import *

def nada_main():
    alice = Party(name="Alice") # party 0 
    bob = Party(name="Bob") # party 1
    charlie = Party(name="Charlie") # party 2

    alice_salary = SecretInteger(Input(name="alice_salary", party=alice))
    bob_salary = SecretInteger(Input(name="bob_salary", party=bob))
    charlie_salary = SecretInteger(Input(name="charlie_salary", party=charlie))

    largest_position = (
        (alice_salary > bob_salary).if_else(
            (alice_salary > charlie_salary).if_else(Integer(0), Integer(2)),
            (bob_salary > charlie_salary).if_else(Integer(1), Integer(2))
        )
    )

    out = Output(largest_position, "largest_position", alice)

    return [out]