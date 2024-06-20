from nada_dsl import *

# Swapping values of variables without using 3rd variable

def nada_main():
    party1=Party(name="Party1")
    a=SecretInteger(Input(name="int1", party=party1))
    b=SecretInteger(Input(name="int2", party=party1))
    
    a=a+b
    b=a-b
    a=a-b 
    
    return [Output(b,"b",party=party1)] 
