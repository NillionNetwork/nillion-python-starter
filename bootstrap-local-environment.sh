#!/usr/bin/env bash

# set number of node and user keys to be created
num_node_keys=5
num_user_keys=5

# set env file to update
ENV_TO_UPDATE=".env"

NILLION_DEVNET="nillion-devnet"
NILLION_CLI="nillion"
NILLION_CLI_COMMAND_USER_KEYGEN="user-key-gen"
NILLION_CLI_COMMAND_NODE_KEYGEN="node-key-gen"

# kill any other nillion-devnet processes
pkill -9 -f $NILLION_DEVNET

for var in NILLION_DEVNET NILLION_CLI; do
  printf "ℹ️ found bin %-18s -> [${!var:?Failed to discover $var}]\n" "$var"
done

OUTFILE=$(mktemp);
PIDFILE=$(mktemp);

"$NILLION_DEVNET" >"$OUTFILE" & echo $! >"$PIDFILE";
echo "--------------------"
echo "Updating your ${ENV_TO_UPDATE} files with nillion-devnet environment info... This may take a minute."
echo "--------------------"
time_limit=160
while true; do
    # Use 'wait' to check if the log file contains the last string output by nillion-devnet
    if grep "environment file written" "$OUTFILE"; then
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

# Extract the path from the line and store it in NILUP_ENV_DIR
NILUP_ENV_DIR=$(grep 'environment file written to' "$OUTFILE" | awk -F' to ' '{print $2}')

get_value_from_nillion_env() {
    # Check if the correct number of arguments are provided
    if [ "$#" -ne 2 ]; then
        echo "Usage: get_value_from_nillion_env <file_path> <key>"
        return 1
    fi

    # Get the file path and key from the arguments
    local FILE_PATH=$1
    local KEY=$2

    # Get the value of the specified key, trimming any whitespace
    local VALUE=$(grep "^$KEY=" "$FILE_PATH" | cut -d'=' -f2 | xargs)

    # Check if the key was found
    if [ -z "$VALUE" ]; then
        echo "Key $KEY not found in $FILE_PATH"
        return 1
    fi

    # Output the value
    echo "$VALUE"
}

# grep cluster info from nillion-devnet
CLUSTER_ID=$(get_value_from_nillion_env "$NILUP_ENV_DIR" "NILLION_CLUSTER_ID")
BOOT_MULTIADDR=$(get_value_from_nillion_env "$NILUP_ENV_DIR" "NILLION_BOOTNODE_MULTIADDRESS")
JSON_RPC=$(get_value_from_nillion_env "$NILUP_ENV_DIR" "NILLION_NILCHAIN_JSON_RPC")
GRPC=$(get_value_from_nillion_env "$NILUP_ENV_DIR" "NILLION_NILCHAIN_GRPC")
WEBSOCKET=$(get_value_from_nillion_env "$NILUP_ENV_DIR" "NILLION_BOOTNODE_WEBSOCKET")
WALLET_PRIVATE_KEY=$(get_value_from_nillion_env "$NILUP_ENV_DIR" "NILLION_NILCHAIN_PRIVATE_KEY_0")

# update or add an environment variable to one or more files
update_env() {
    local key=$1
    local value=$2
    # Skip the first two arguments to get the file paths
    local files=("${@:3}")

    for file in "${files[@]}"; do
        if [ -f "$file" ]; then  # Check if file exists
            # Check if the key exists in the file and remove it
            if grep -q "^$key=" "$file"; then
                # Key exists, remove it
                grep -v "^$key=" "$file" > temp.txt && mv temp.txt "$file"
            fi

            # Append the new key-value pair to the file
            echo "$key=$value" >> "$file"
        else
            echo "File $file not found. Creating $file"
            touch $file
            echo "$key=$value" >> "$file"
        fi
    done
}

# log file contents of key files to add to .env
log_file_contents() {
    local file_path=$1  # Direct path to the target file

    # Check if the file exists at the path
    if [[ ! -f "$file_path" ]]; then
        echo "File $file_path does not exist."
        return 1  # Exit the function with an error status if the file does not exist
    fi

    # If the file exists, cat its contents
    cat "$file_path"
}

# Generate node keys and add to .env - ex: NILLION_NODEKEY_PATH_PARTY_1
for ((i=1; i<=$num_node_keys; i++)); do
    nodekey_file=$(mktemp)
    "$NILLION_CLI" "$NILLION_CLI_COMMAND_NODE_KEYGEN" "$nodekey_file"
    NODEKEY_FILES+=("$nodekey_file")
    update_env "NILLION_NODEKEY_PATH_PARTY_$i" "$nodekey_file" $ENV_TO_UPDATE
    update_env "NILLION_NODEKEY_TEXT_PARTY_$i" "$(log_file_contents $nodekey_file)" $ENV_TO_UPDATE
done

# Generate user keys and add to .env - ex: NILLION_USERKEY_PATH_PARTY_1
for ((i=1; i<=$num_user_keys; i++)); do
    userkey_file=$(mktemp)
    "$NILLION_CLI" "$NILLION_CLI_COMMAND_USER_KEYGEN" "$userkey_file"
    USERKEY_FILES+=("$userkey_file")
    update_env "NILLION_USERKEY_PATH_PARTY_$i" "$userkey_file" $ENV_TO_UPDATE
    update_env "NILLION_USERKEY_TEXT_PARTY_$i" "$(log_file_contents $userkey_file)" $ENV_TO_UPDATE
done

echo "🔑 Node key and user keys have been generated and added to .env"

# Add environment variables to .env
update_env "NILLION_WEBSOCKETS" "$WEBSOCKET" $ENV_TO_UPDATE
update_env "NILLION_CLUSTER_ID" "$CLUSTER_ID" $ENV_TO_UPDATE
update_env "NILLION_BOOTNODE_MULTIADDRESS" "$BOOT_MULTIADDR" $ENV_TO_UPDATE
update_env "NILLION_JSON_RPC" "$JSON_RPC" $ENV_TO_UPDATE
update_env "NILLION_GRPC" "$GRPC" $ENV_TO_UPDATE
update_env "NILLION_CHAIN_ID" "nillion-chain-testnet" $ENV_TO_UPDATE
update_env "NILLION_WALLET_PRIVATE_KEY" "$WALLET_PRIVATE_KEY" $ENV_TO_UPDATE

echo "Running at process pid: $(pgrep -f $NILLION_DEVNET)"

echo "-------------------------------------------------------"
echo "                   7MM   7MM                           "
echo "                    MM    MM                           "
echo "              db    MM    MM    db                     "
echo "                    MM    MM                           "
echo ".7MMpMMMb.   7MM    MM    MM   7MM  ,pW-Wq. 7MMpMMMb.  "
echo "  MM    MM    MM    MM    MM    MM 6W'    Wb MM    MM  "
echo "  MM    MM    MM    MM    MM    MM 8M     M8 MM    MM  "
echo "  MM    MM    MM    MM    MM    MM YA.   ,A9 MM    MM  "
echo ".JMML  JMML..JMML..JMML..JMML..JMML. Ybmd9 .JMML  JMML."
echo "-------------------------------------------------------"
echo "-------------------------------------------------------"
echo "-----------🦆 CONNECTED TO NILLION-DEVNET 🦆-----------"
echo "-------------------------------------------------------"

echo "ℹ️ Your $ENV_TO_UPDATE file configurations were updated with nillion-devnet connection variables: websocket, cluster id, keys, blockchain info"
echo "💻 The Nillion devnet is still running behind the scenes; to spin down the Nillion devnet at any time, run 'killall nillion-devnet'"

echo "--------------------"
echo "💻 Your Nillion local cluster is still running - process pid: $(pgrep -f $NILLION_DEVNET)"
echo "ℹ️  Updated your .env file configuration variables: bootnode, cluster id, keys, blockchain info"

exit 0
