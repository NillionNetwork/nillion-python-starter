#!/usr/bin/env bash
THIS_SCRIPT_DIR="$(dirname "$0")"

set -euo pipefail
trap "kill 0" SIGINT SIGTERM SIGQUIT EXIT

# shellcheck source=../utils.sh
source "$THIS_SCRIPT_DIR/../utils.sh"

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

trap 'kill $(pidof $RUN_LOCAL_CLUSTER)' SIGINT SIGTERM SIGQUIT EXIT

NODEKEYFILE=$(mktemp);
READERKEYFILE=$(mktemp);
WRITERKEYFILE=$(mktemp);
NILLION_CONFIG=$(mktemp);
export NILLION_CONFIG

SEED_PHRASE="$0";

if pidof "$RUN_LOCAL_CLUSTER" > /dev/null; then
  __echo_red_bold "⚠️ $RUN_LOCAL_CLUSTER is already running! It is unlikely you want this, consider terminating that process and re-running this test."
fi

"$RUN_LOCAL_CLUSTER" --seed "$SEED_PHRASE" >"$OUTFILE" & echo $! >"$PIDFILE";

time_limit=40
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

CLUSTER_ID=$(grep -oP 'cluster id is \K.*' "$OUTFILE");
BOOT_MULTIADDR=$(grep -oP 'bootnode is at \K.*' "$OUTFILE");
PAYMENTS_CONFIG_FILE=$(grep -oP 'payments configuration written to \K.*' "$OUTFILE");
WALLET_KEYS_FILE=$(grep -oP 'wallet keys written to \K.*' "$OUTFILE");

PAYMENTS_RPC=$(grep -oP 'blockchain_rpc_endpoint: \K.*' "$PAYMENTS_CONFIG_FILE");
PAYMENTS_CHAIN=$(grep -oP 'chain_id: \K.*' "$PAYMENTS_CONFIG_FILE");
PAYMENTS_SC_ADDR=$(grep -oP 'payments_sc_address: \K.*' "$PAYMENTS_CONFIG_FILE");
PAYMENTS_BF_ADDR=$(grep -oP 'blinding_factors_manager_sc_address: \K.*' "$PAYMENTS_CONFIG_FILE");

WALLET_PRIVATE_KEY=$(tail -n1 "$WALLET_KEYS_FILE")

echo "ℹ️ Cluster has been STARTED (see $OUTFILE)"
cat "$OUTFILE"

"$NODE_KEYGEN" "$NODEKEYFILE"
"$USER_KEYGEN" "$READERKEYFILE"
"$USER_KEYGEN" "$WRITERKEYFILE"

echo "🔑 Keys have been generated"

echo "💤 sleeping for 10 seconds to enable alpha generation"
sleep 10;

jq -n \
    --arg bootnode "$BOOT_MULTIADDR" \
    --arg cluster "$CLUSTER_ID" \
    --arg writerkey "$WRITERKEYFILE" \
    --arg readerkey "$READERKEYFILE" \
    --arg nodekey "$NODEKEYFILE" \
    --arg blockchain_rpc_endpoint "$PAYMENTS_RPC" \
    --arg chain_id "$PAYMENTS_CHAIN" \
    --arg payments_sc_address "$PAYMENTS_SC_ADDR" \
    --arg blinding_factors_manager_sc_address "$PAYMENTS_BF_ADDR" \
    --arg wallet_private_key "$WALLET_PRIVATE_KEY" \
    '{
        YOUR_BOOTNODE_MULTIADDRESS_HERE: $bootnode,
        YOUR_CLUSTER_ID_HERE: $cluster,
        YOUR_WRITERKEY_PATH_HERE: $writerkey,
        YOUR_READERKEY_PATH_HERE: $readerkey,
        YOUR_NODEKEY_PATH_HERE: $nodekey,
        YOUR_BLOCKCHAIN_RPC_ENDPOINT: $blockchain_rpc_endpoint,
        YOUR_CHAIN_ID: $chain_id,
        YOUR_PAYMENTS_SC_ADDRESS: $payments_sc_address,
        YOUR_BLINDING_FACTORS_MANAGER_SC_ADDRESS: $blinding_factors_manager_sc_address,
        YOUR_WALLET_PRIVATE_KEY: $wallet_private_key
    }' >"$NILLION_CONFIG"
echo "ℹ️  injected program, bootnode and cluster_id into config: [$NILLION_CONFIG]";

echo "ℹ️  starting python test";

PEER_USERID=$(python3 01-fetch-reader-userid.py)
echo "ℹ️  got reader PEER_USERID: [$PEER_USERID]"

STORE_ID=$(python3 02-store-secret.py --reader_user_id "$PEER_USERID")
echo "ℹ️  got secret STORE_ID: [$STORE_ID]"

python3 03-retrieve-secret.py --store_id "$STORE_ID"
python3 04-revoke-read-permissions.py --store_id "$STORE_ID" --reader_user_id "$PEER_USERID"
python3 05-revoked-permissions-test.py --store_id "$STORE_ID"

exit 0
