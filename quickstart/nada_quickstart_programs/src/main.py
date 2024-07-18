import random

def guess_number():
    # Generate a random number between 1 and 100
    number_to_guess = random.randint(1, 100)
    guess = None
    attempts = 0
    
    print("I'm thinking of a number between 1 and 100. Try to guess it!")

    while guess != number_to_guess:
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
        
        except ValueError:
            print("Please enter a valid number.")

guess_number()

