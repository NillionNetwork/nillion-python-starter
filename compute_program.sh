#!/bin/bash

PROGRAM_ID="5RPtfEpCfDuGYiXAtxhywxVZfUqFojUZhuscEbtus1ufU7GPDfscJhQyDwdTmCXvpcSgc6zLix5PZYG4Ddjua6mF/addition_simple"

STORE_ID="9632cb80-0355-4680-8fce-48d14ace085f"

# This script stores a compiled program
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}" 2>/dev/null)" && pwd -P)"

set -a  # Automatically export all variables
source "$SCRIPT_PATH/.env"
set +a  # Stop automatically exporting

$NILLION_SDK_ROOT/nil-cli \
    --user-key-path $NILLION_WRITERKEY_PATH \
    --node-key-path $NILLION_NODEKEY_PATH \
    -b $NILLION_BOOTNODE_MULTIADDRESS \
    --payments-private-key $NILLION_WALLET_PRIVATE_KEY \
    --payments-chain-id $NILLION_CHAIN_ID \
    --payments-rpc-endpoint $NILLION_BLOCKCHAIN_RPC_ENDPOINT \
    --payments-sc-address $NILLION_PAYMENTS_SC_ADDRESS \
    --blinding-factors-manager-sc-address $NILLION_BLINDING_FACTORS_MANAGER_SC_ADDRESS \
    compute \
    --cluster-id $NILLION_CLUSTER_ID \
    --store-id $STORE_ID \
    --result-node-name "Party1" \
    $PROGRAM_ID