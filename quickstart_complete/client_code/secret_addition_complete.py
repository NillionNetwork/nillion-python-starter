from nada_dsl import *
from nada_program import nada_main  # Adjust import based on your file structure

def main():
    # Initialize parties
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    party3 = Party(name="Party3")
    
    # Initialize inputs
    number = 16  # Example input for square root calculation
    
    # Run the program
    program = nada_main()  # Adjust based on your program setup
    
    # Define a function for executing the square root program
    def execute_program(program, number):
        # This part depends on how you integrate with NADA and the specifics of your program
        return program.find_square_root(number)
    
    # Execute the program with the input
    result = execute_program(program, number)
    
    # Print the result
    print(f"The square root of {number} is {result}.")

if __name__ == "__main__":
    main()
