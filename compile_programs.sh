#!/usr/bin/env bash

# This script compiles all $PROGRAMS_FOLDER programs to mir
PROGRAMS_FOLDER="programs"
COMPILED_PROGRAMS_FOLDER="programs-compiled"

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}" 2>/dev/null)" && pwd -P)"
TARGET_PATH="${SCRIPT_PATH}/${COMPILED_PROGRAMS_FOLDER}"
PROGRAMS_PATH="${SCRIPT_PATH}/${PROGRAMS_FOLDER}"

# shellcheck source=utils.sh
source "$SCRIPT_PATH/utils.sh"

# shellcheck source=activate_venv.sh
source "$SCRIPT_PATH/activate_venv.sh"

set -a  # Automatically export all variables
source "$SCRIPT_PATH/.env"
set +a  # Stop automatically exporting

check_for_sdk_root
install_nada_dsl

PYNADAC="$(discover_sdk_bin_path pynadac)"

cd "${PROGRAMS_PATH}" || exit 1

for file in *.py ; do
  echo "Compiling ${file}"
  "$PYNADAC" --target-dir "${TARGET_PATH}" \
    --generate-mir-json \
    "${file}"
done 

echo "COMPLETE: all files in the programs directory were compiled to mir: [$TARGET_PATH]"
echo "To store a compiled program, run './store_program.sh programs-compiled/{program_name}.nada.bin'"
echo "📋 Store the addition_simple program: './store_program.sh programs-compiled/addition_simple.nada.bin'"