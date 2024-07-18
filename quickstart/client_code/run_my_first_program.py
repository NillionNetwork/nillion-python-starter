# Function to calculate factorial
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

# Main function
def main():
    # Prompt the user to enter a number
    number = int(input("Enter a number to calculate its factorial: "))

    # Calculate the factorial using the function
    result = factorial(number)

    # Print the result
    print(f"The factorial of {number} is {result}")

# Run the main function
if __name__ == "__main__":
    main()
