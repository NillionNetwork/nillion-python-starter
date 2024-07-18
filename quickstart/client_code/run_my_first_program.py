from nada_dsl import *

def nada_main():
    # Define the party
    party1 = Party(name="Party1")

    # Input the credit card number from the party
    cc_number = SecretString(Input(name="cc_number", party=party1))

    # Convert the string to a list of integers
    digits = [SecretInteger(int(digit)) for digit in cc_number]

    # Reverse the digits for easier processing
    reversed_digits = digits[::-1]

    # Double every second digit from the right
    doubled_digits = []
    for i, digit in enumerate(reversed_digits):
        if i % 2 == 1:
            doubled_digit = digit * 2
            if doubled_digit > 9:
                doubled_digit = doubled_digit - 9
            doubled_digits.append(doubled_digit)
        else:
            doubled_digits.append(digit)

    # Sum all the digits
    total_sum = sum(doubled_digits)

    # Check if the total sum modulo 10 is 0
    is_valid = SecretBoolean(total_sum % 10 == 0)

    # Return the result
    return [Output(is_valid, "is_valid_output", party1)]
