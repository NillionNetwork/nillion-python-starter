import os
import py_nillion_client as nillion

def create_payments_config():
    return nillion.PaymentsConfig(
        os.getenv("YOUR_BLOCKCHAIN_RPC_ENDPOINT"),
        os.getenv("YOUR_WALLET_PRIVATE_KEY"),
        int(os.getenv("YOUR_CHAIN_ID")),
        os.getenv("YOUR_PAYMENTS_SC_ADDRESS"),
        os.getenv("YOUR_BLINDING_FACTORS_MANAGER_SC_ADDRESS"),
    )
