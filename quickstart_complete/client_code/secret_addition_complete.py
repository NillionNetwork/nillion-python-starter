# /content/nillion-python-starter/quickstart/client_code/run_my_first_program.py

from quickstart.my_first_program import fibonacci

def main():
    n = 10  # Number of Fibonacci numbers to generate
    result = fibonacci(n)
    print("The first", n, "Fibonacci numbers are:", result)

if __name__ == "__main__":
    main()
