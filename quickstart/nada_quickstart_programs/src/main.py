from nada_dsl import *

def nada_main():
    # Define the parties for the ATM users
    atm_user_1 = Party(name="ATM User 1 💳")
    atm_user_2 = Party(name="ATM User 2 💳")

    # Define secret inputs for the initial balances, deposit amounts, withdrawal amounts, and transfer amounts
    initial_balance_1 = SecretInteger(Input(name="initial_balance_1", party=atm_user_1))
    initial_balance_2 = SecretInteger(Input(name="initial_balance_2", party=atm_user_2))
    deposit_amount_1 = SecretInteger(Input(name="deposit_amount_1", party=atm_user_1))
    withdrawal_amount_1 = SecretInteger(Input(name="withdrawal_amount_1", party=atm_user_1))
    transfer_amount_1_to_2 = SecretInteger(Input(name="transfer_amount_1_to_2", party=atm_user_1))

    # Calculate the new balance for ATM User 1 after deposit
    balance_after_deposit_1 = initial_balance_1 + deposit_amount_1

    # Ensure the withdrawal does not exceed the balance after deposit for ATM User 1
    sufficient_funds_after_withdrawal_1 = (balance_after_deposit_1 >= withdrawal_amount_1).if_else(
        balance_after_deposit_1 - withdrawal_amount_1,
        balance_after_deposit_1
    )

    # Ensure the transfer does not exceed the balance after withdrawal for ATM User 1
    sufficient_funds_after_transfer_1 = (sufficient_funds_after_withdrawal_1 >= transfer_amount_1_to_2).if_else(
        sufficient_funds_after_withdrawal_1 - transfer_amount_1_to_2,
        sufficient_funds_after_withdrawal_1
    )

    # Calculate the new balance for ATM User 2 after receiving the transfer
    balance_after_transfer_2 = initial_balance_2 + transfer_amount_1_to_2

    # Output the final balances for both users
    final_balance_1 = Output(sufficient_funds_after_transfer_1, "final_balance_1", atm_user_1)
    final_balance_2 = Output(balance_after_transfer_2, "final_balance_2", atm_user_2)

    return [final_balance_1, final_balance_2]

