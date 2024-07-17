from nada_dsl import *

def nada_main():
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")
    party3 = Party(name="Party3")
    
    length = SecretInteger(Input(name="Length", party=party1))
    breadth = SecretInteger(Input(name="Breadth", party=party2))

    area = length * breadth

    return [Output(area, "rectangle_area", party3)]
