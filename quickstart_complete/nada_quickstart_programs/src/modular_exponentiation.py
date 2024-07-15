import numpy as np
from nada_dsl import *

import nada_numpy as na

LOG_SCALE = 16
SCALE = 1 << LOG_SCALE
PRIME_64 = 18446744072637906947
PRIME_128 = 340282366920938463463374607429104828419
PRIME_256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF98C00003
PRIME = PRIME_64

def public_modular_exponentiation(base: PublicInteger | Integer, exponent: PublicInteger | Integer, modulo: int) -> PublicInteger | Integer:
    # Compute base^exponent % modulo using public integers
    return (base ** exponent) % Integer(modulo)

def private_modular_exponentiation(base: SecretInteger, exponent: SecretInteger, modulo: int) -> SecretInteger:
    # Generate random masks for the base and exponent
    r_base = SecretInteger.random()
    r_exponent = SecretInteger.random()

    # Mask the base and exponent
    masked_base = r_base * base
    masked_exponent = r_exponent * exponent

    # Reveal the masked values for computation
    masked_base_revealed = masked_base.reveal()
    masked_exponent_revealed = masked_exponent.reveal()

    # Compute the modular exponentiation of the masked values
    mod_exp = public_modular_exponentiation(masked_base_revealed, masked_exponent_revealed, modulo)

    # Unmask the result
    result = mod_exp * r_base * r_exponent

    return result

def nada_main():
    # Initialize three parties
    parties = na.parties(3)

    # Receive base from Party 0 and exponent from Party 1
    base = na.array([2], parties[0], "Base", nada_type=SecretInteger)
    exponent = na.array([3], parties[1], "Exponent", nada_type=SecretInteger)

    # Compute private modular exponentiation
    mod_exp_result = private_modular_exponentiation(base[0], exponent[0], PRIME)

    # Output the result to Party 2
    return na.output(mod_exp_result, parties[2], "ModExpOutput")
