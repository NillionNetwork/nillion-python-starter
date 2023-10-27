#!/usr/bin/env bash

function install_nada_dsl() {
  WHLPATH=$(find "$NILLION_SDK_ROOT" -name "nada_dsl-*-any.whl" -type f -print | head -n1)
  pip install "$WHLPATH"
}

function discover_sdk_bin_path() {
  BINPATH=$(find "$NILLION_SDK_ROOT" -name "$1" -type f -executable -print | head -n1)
  if ! command -v "$BINPATH" > /dev/null; then
    echo "${1} was not discovered. Check NILLION_SDK_ROOT" 1>&2
    exit 1
  fi
  echo "$BINPATH"
}

function check_for_sdk_root() {
  if [ -z "$NILLION_SDK_ROOT" -a ! -d "$NILLION_SDK_ROOT" ]; then
    echo "Error: NILLION_SDK_ROOT is not set to a directory"
    exit 1
  fi
}
