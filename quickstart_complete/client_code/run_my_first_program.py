import numpy as np
from nada_dsl import *

import nada_numpy as na

LOG_SCALE = 16
SCALE = 1 << LOG_SCALE
PRIME_64 = 18446744072637906947
PRIME_128 = 340282366920938463463374607429104828419
PRIME_256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF98C00003
PRIME = PRIME_64

def public_modular_exponentiation(
    base: PublicInteger | Integer, exponent: PublicInteger | Integer, modulo: int
) -> PublicInteger | Integer:
    """
    Calculates the modular exponentiation of a public base raised to a public exponent with respect to a prime modulus.

    Args:
        `base`: The base to be exponentiated.
        `exponent`: The exponent to raise the base to.
        `modulo`: The prime modulo with respect to which the exponentiation is to be calculated.

    Returns:
        The result of the modular exponentiation.

    Raises:
        Exception: If the input type is not a `PublicInteger` or `Integer`.
    """
    return (base ** exponent) % Integer(modulo)


def private_modular_exponentiation(
    base: SecretInteger, exponent: SecretInteger, modulo: int
) -> SecretInteger:
    """
    Calculate the modular exponentiation of a secret base raised to a secret exponent with respect to a prime modulo.

    Args:
        base (SecretInteger): The base to be exponentiated.
        exponent (SecretInteger): The exponent to raise the base to.
        modulo (int): The prime modulo with respect to which the exponentiation is to be calculated.

    Returns:
        SecretInteger: The result of the modular exponentiation.
    """
    r_base = SecretInteger.random()
    r_exponent = SecretInteger.random()

    masked_base = r_base * base  # Masking our base
    masked_exponent = r_exponent * exponent  # Masking our exponent

    masked_base_revealed = masked_base.reveal()  # Revealing the masked base
    masked_exponent_revealed = masked_exponent.reveal()  # Revealing the masked exponent

    mod_exp = public_modular_exponentiation(
        masked_base_revealed, masked_exponent_revealed, modulo
    )  # Compute the exponentiation of the masked base and exponent

    result = mod_exp * r_base * r_exponent  # Unmask the result with the random shares

    return result

def nada_main():
    parties = na.parties(3)

    base = na.array([2], parties[0], "Base", nada_type=SecretInteger)
    exponent = na.array([3], parties[1], "Exponent", nada_type=SecretInteger)
    mod_exp_result = private_modular_exponentiation(base[0], exponent[0], PRIME)

    return na.output(mod_exp_result, parties[2], "ModExpOutput")
