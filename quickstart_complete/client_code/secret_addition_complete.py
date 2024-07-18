from nillion import Client  # Assuming `nillion` is the module being used

def main():
    # Initialize the client
    client = Client()

    # Your program's specific functionality
    # For example, if your program calculates factorial:
    number = 5  # Example number
    result = client.factorial(number)  # Call your program's function
    
    # Print the result
    print(f"The factorial of {number} is {result}")

if __name__ == "__main__":
    main()
