#!/usr/bin/env bash
THIS_SCRIPT_DIR="$(dirname "$0")"

set -euo pipefail
trap "kill 0" SIGINT SIGTERM SIGQUIT EXIT

# shellcheck source=./utils.sh
source "$THIS_SCRIPT_DIR/utils.sh"

set -a  # Automatically export all variables
source "$THIS_SCRIPT_DIR/.env"
set +a  # Stop automatically exporting

check_for_sdk_root
install_nada_dsl
install_py_nillion_client

RUN_LOCAL_CLUSTER="$(discover_sdk_bin_path run-local-cluster)"
USER_KEYGEN=$(discover_sdk_bin_path user-keygen)
NODE_KEYGEN=$(discover_sdk_bin_path node-keygen)

for var in RUN_LOCAL_CLUSTER USER_KEYGEN NODE_KEYGEN; do
  printf "ℹ️ found bin %-18s -> [${!var:?Failed to discover $var}]\n" "$var"
done

OUTFILE=$(mktemp);
PIDFILE=$(mktemp);

echo $OUTFILE

trap 'kill $(pidof $RUN_LOCAL_CLUSTER)' SIGINT SIGTERM SIGQUIT EXIT

NODEKEYFILE=$(mktemp);
READERKEYFILE=$(mktemp);
WRITERKEYFILE=$(mktemp);

"$RUN_LOCAL_CLUSTER" >"$OUTFILE" & echo $! >"$PIDFILE";

time_limit=160
while true; do
    # Use 'wait' to check if the log file contains the string
    if grep "cluster is running, bootnode is at" "$OUTFILE"; then
        break
    fi

    # If the time limit has been reached, print an error message and exit
    if [[ $SECONDS -ge $time_limit ]]; then
        echo "Timeout reached while waiting for cluster to be ready in '$OUTFILE'" >&2
        exit 1
    fi
    sleep 5
done

echo "ℹ️ Cluster has been STARTED (see $OUTFILE)"
cat "$OUTFILE"

CLUSTER_ID=$(grep "cluster id is" "$OUTFILE" | awk '{print $4}');
BOOT_MULTIADDR=$(grep "cluster is running, bootnode is at" "$OUTFILE" | awk '{print $7}');
PAYMENTS_CONFIG_FILE=$(grep "payments configuration written to" "$OUTFILE" | awk '{print $5}');
WALLET_KEYS_FILE=$(grep "wallet keys written to" "$OUTFILE" | awk '{print $5}');
PAYMENTS_RPC=$(grep "blockchain_rpc_endpoint:" "$PAYMENTS_CONFIG_FILE" | awk '{print $2}');
PAYMENTS_CHAIN=$(grep "chain_id:" "$PAYMENTS_CONFIG_FILE" | awk '{print $2}');
PAYMENTS_SC_ADDR=$(grep "payments_sc_address:" "$PAYMENTS_CONFIG_FILE" | awk '{print $2}');
PAYMENTS_BF_ADDR=$(grep "blinding_factors_manager_sc_address:" "$PAYMENTS_CONFIG_FILE" | awk '{print $2}');
WALLET_PRIVATE_KEY=$(tail -n1 "$WALLET_KEYS_FILE")

echo "🔑 Generating a node key and user keys (reader key and writer key)"

"$NODE_KEYGEN" "$NODEKEYFILE"
"$USER_KEYGEN" "$READERKEYFILE"
"$USER_KEYGEN" "$WRITERKEYFILE"

echo "🔑 Keys have been generated"


# Function to update or add an environment variable in the .env file
update_env() {
    local key=$1
    local value=$2
    local file="./.env"  # Path to the .env file

    # Check if the key exists in the file and remove it
    if grep -q "^$key=" "$file"; then
        # Key exists, remove it
        grep -v "^$key=" "$file" > temp.txt && mv temp.txt "$file"
    fi

    # Append the new key-value pair to the file
    echo "$key=$value" >> "$file"
}

# Add environment variables to .env
update_env "NILLION_BOOTNODE_MULTIADDRESS" "$BOOT_MULTIADDR"
update_env "NILLION_CLUSTER_ID" "$CLUSTER_ID"
update_env "NILLION_WRITERKEY_PATH" "$WRITERKEYFILE"
update_env "NILLION_READERKEY_PATH" "$READERKEYFILE"
update_env "NILLION_NODEKEY_PATH" "$NODEKEYFILE"
update_env "NILLION_BLOCKCHAIN_RPC_ENDPOINT" "$PAYMENTS_RPC"
update_env "NILLION_CHAIN_ID" "$PAYMENTS_CHAIN"
update_env "NILLION_PAYMENTS_SC_ADDRESS" "$PAYMENTS_SC_ADDR"
update_env "NILLION_BLINDING_FACTORS_MANAGER_SC_ADDRESS" "$PAYMENTS_BF_ADDR"
update_env "NILLION_WALLET_PRIVATE_KEY" "$WALLET_PRIVATE_KEY"
echo "ℹ️  Updated configuration variables (bootnode, cluster id, keys, blockchain info) in the .env file."

echo "📋 To start python permissions examples, run 'cd permissions && python3 01-fetch-reader-userid.py' to get the reader user id";

exit 0