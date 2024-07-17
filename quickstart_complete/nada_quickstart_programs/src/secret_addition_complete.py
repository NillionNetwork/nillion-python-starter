from nada_dsl import *
def nada_main():

    party1 = Party(name="Party1")

    # Define a list of secret integers as inputs
    secret_integers = [
        SecretInteger(Input(name=f"int{i+1}", party=party1)) 
        for i in range(5)  # Let's assume we are taking 5 integers for simplicity
    ]

    # Calculate the sum of the secret integers
    total_sum = sum(secret_integers)

    # Calculate the average
    average = total_sum / len(secret_integers)

    return [Output(average, "average_output", party1)]
