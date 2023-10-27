#!/usr/bin/env bash


SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}" 2>/dev/null)" && pwd -P)"
TARGET_PATH="${SCRIPT_PATH}/target"
PROGRAMS_PATH="${SCRIPT_PATH}/programs"

# shellcheck source=utils.sh
source "$SCRIPT_PATH/utils.sh"

# shellcheck source=activate_venv.sh
source "$SCRIPT_PATH/activate_venv.sh"

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

echo "COMPLETE: programs compiled to mir in dir: [$TARGET_PATH]"
