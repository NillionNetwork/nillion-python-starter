from nada_dsl import *

def nada_main():
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")

    dramaP1 = SecretInteger(Input(name="DramaP1", party=party1))
    actionP1 = SecretInteger(Input(name="ActionP1", party=party1))
    horrorP1 = SecretInteger(Input(name="HorrorP1", party=party1))
    romanceP1 = SecretInteger(Input(name="RomanceP1", party=party1))
    thrillerP1 = SecretInteger(Input(name="ThrillerP1", party=party1))
    comedyP1 = SecretInteger(Input(name="ComedyP1", party=party1))

    dramaP2 = SecretInteger(Input(name="DramaP2", party=party2))
    actionP2 = SecretInteger(Input(name="ActionP2", party=party2))
    horrorP2 = SecretInteger(Input(name="HorrorP2", party=party2))
    romanceP2 = SecretInteger(Input(name="RomanceP2", party=party2))
    thrillerP2 = SecretInteger(Input(name="ThrillerP2", party=party2))
    comedyP2 = SecretInteger(Input(name="ComedyP2", party=party2))
    
    div = Integer(0)
    ans = Integer(0)

    u1 = [dramaP1, actionP1, horrorP1, romanceP1, thrillerP1, comedyP1] 
    u2 = [dramaP2, actionP2, horrorP2, romanceP2, thrillerP2, comedyP2]

    #checks the difference between choice and calculates the score
    for x in range(6):
        t = u1[x] - u2[x]
        if t < Integer(0):
            t = t * Integer(-1)
        ans = ans + t
        if u1[x] > Integer(0) or u2[x] > Integer(0):
            div = div + Integer(5)

    # using finite field method to divide the ans and calculate percentage
    inverse_mod = (div ** (Integer(29))) % Integer(31)
    result = Integer(100) - ((ans * Integer(7) * inverse_mod) % Integer(31))

    return [Output(result, "buddy_score", party1), Output(result, "buddy_score", party2)]