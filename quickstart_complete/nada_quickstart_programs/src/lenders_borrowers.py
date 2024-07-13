from nada_dsl import *

def nada_main():

    # 0. Constants for configuration
    number_of_lenders = 3
    number_of_borrowers = 2

    # 1. Initialize parties
    lender_parties = [
        Party(name=f"LenderParty{idx}") for idx in range(number_of_lenders)
    ]
    borrower_parties = [
        Party(name=f"BorrowerParty{idx}") for idx in range(number_of_borrowers)
    ]
    result_party = Party(name="ResultParty")

    # 2. Initialize inputs
    # loans[lender][borrower] is the amount lent by lender to borrower
    loans = [
        [
            SecretUnsignedInteger(
                Input(name=f"loan_lender_{lender}_borrower_{borrower}", party=lender_parties[lender])
            ) for borrower in range(number_of_borrowers)
        ] for lender in range(number_of_lenders)
    ]

    # 3. Calculate total amounts lent by each lender
    total_amounts_lent = []
    for lender in range(number_of_lenders):
        total_lent = loans[lender][0]
        for borrower in range(1, number_of_borrowers):
            total_lent += loans[lender][borrower]
        # Output total amount lent by lender
        total_amounts_lent.append(
            Output(total_lent, f"total_amount_lent_by_lender_{lender}", result_party)
        )

    # 4. Calculate total amounts borrowed by each borrower
    total_amounts_borrowed = []
    for borrower in range(number_of_borrowers):
        total_borrowed = loans[0][borrower]
        for lender in range(1, number_of_lenders):
            total_borrowed += loans[lender][borrower]
        # Output total amount borrowed by borrower
        total_amounts_borrowed.append(
            Output(total_borrowed, f"total_amount_borrowed_by_borrower_{borrower}", result_party)
        )

    return total_amounts_lent + total_amounts_borrowed

