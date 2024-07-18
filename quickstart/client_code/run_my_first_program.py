import math

def find_square_root(number):
    if number < 0:
        return "Square root of negative numbers is not defined in the real number system."
    return math.sqrt(number)

def main():
    try:
        number = float(input("Enter a number to find its square root: "))
        result = find_square_root(number)
        print(f"The square root of {number} is {result}.")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()
