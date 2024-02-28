#!/usr/bin/env bash
THIS_SCRIPT_DIR="$(dirname "$0")"

set -euo pipefail

# shellcheck source=./utils.sh
source "$THIS_SCRIPT_DIR/utils.sh"

set -a  # Automatically export all variables
source "$THIS_SCRIPT_DIR/.env"
set +a  # Stop automatically exporting

# Install Nada DSL, Py Nillion Client, and requirements
check_for_sdk_root
install_nada_dsl
install_py_nillion_client
pip install -r requirements.txt