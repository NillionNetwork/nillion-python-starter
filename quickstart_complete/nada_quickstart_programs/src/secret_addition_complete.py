from nada_dsl import *

def nada_main():
    # Define the party
    party1 = Party(name="Party1")

    # Input the string from the party
    input_str = SecretString(Input(name="input_str", party=party1))

    # Reverse the string
    reversed_str = SecretString(input_str[::-1])

    # Check if the input string is equal to the reversed string
    is_palindrome = SecretBoolean(input_str == reversed_str)

    # Return the result
    return [Output(is_palindrome, "is_palindrome_output", party1)]
