from nada_dsl import *

def nada_main():
    # Define three parties
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    party3 = Party(name="Party3")
    
    # Define secret integers from party1 and party2
    a = SecretInteger(Input(name="A", party=party1))
    b = SecretInteger(Input(name="B", party=party2))
    
    # Perform a secure computation (addition in this case)
    result = a + b
    
    # Output the result to party3
    return [Output(result, "my_output", party3)]
