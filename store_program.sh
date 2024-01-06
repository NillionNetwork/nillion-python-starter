#!/bin/bash

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}" 2>/dev/null)" && pwd -P)"

set -a  # Automatically export all variables
source "$SCRIPT_PATH/.env"
set +a  # Stop automatically exporting

# Check for the correct number of arguments
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <RELATIVE_PROGRAM_PATH>"
    exit 1
fi

RELATIVE_PROGRAM_PATH="$SCRIPT_PATH/$1"
# Extract the program name from the path (e.g., addition_simple from ./programs-compiled/addition_simple.nada.bin)
PROGRAM_NAME=$(basename "$RELATIVE_PROGRAM_PATH" .nada.bin)

# Execute the command
$NILLION_SDK_ROOT/nil-cli \
    --user-key-path $NILLION_WRITERKEY_PATH \
    --node-key-path $NILLION_NODEKEY_PATH \
    -b $NILLION_BOOTNODE_MULTIADDRESS \
    --payments-private-key $NILLION_WALLET_PRIVATE_KEY \
    --payments-chain-id $NILLION_CHAIN_ID \
    --payments-rpc-endpoint $NILLION_BLOCKCHAIN_RPC_ENDPOINT \
    --payments-sc-address $NILLION_PAYMENTS_SC_ADDRESS \
    --blinding-factors-manager-sc-address $NILLION_BLINDING_FACTORS_MANAGER_SC_ADDRESS \
    store-program \
    --cluster-id $NILLION_CLUSTER_ID \
    $RELATIVE_PROGRAM_PATH \
    $PROGRAM_NAME