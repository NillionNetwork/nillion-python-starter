import random

def guess_number():
    # Get the range from the user
    while True:
        try:
            low = int(input("Enter the lower bound of the range: "))
            high = int(input("Enter the upper bound of the range: "))
            if low >= high:
                print("The upper bound must be greater than the lower bound. Please try again.")
            else:
                break
        except ValueError:
            print("Please enter valid integers for the range.")

    # Generate a random number within the chosen range
    number_to_guess = random.randint(low, high)
    guess = None
    attempts = 0
    max_attempts = 10

    print(f"I'm thinking of a number between {low} and {high}. Try to guess it!")

    while guess != number_to_guess and attempts < max_attempts:
        try:
            # Get the user's guess
            guess = int(input("Enter your guess: "))
            attempts += 1

            if guess < number_to_guess:
                print("Too low! Try again.")
            elif guess > number_to_guess:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
                break
        except ValueError:
            print("Please enter a valid number.")

    if guess != number_to_guess:
        print(f"Sorry, you've used all {max_attempts} attempts. The number was {number_to_guess}.")

guess_number()

