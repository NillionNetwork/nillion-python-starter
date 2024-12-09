def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Error! Division by zero."

def calculator():
    print("Select operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    
    choice = input("Enter choice (1/2/3/4): ")
    
    if choice in ('1', '2', '3', '4'):
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        operations = {
            '1': add,
            '2': subtract,
            '3': multiply,
            '4': divide
        }
        
        result = operations[choice](num1, num2)
        print(f"The result is: {result}")
    else:
        print("Invalid input")

if __name__ == "__main__":
    calculator()
