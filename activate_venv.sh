#!/usr/bin/env bash

function deactivate_venv() {
    echo "Deactivating virtualenv"
    deactivate
}

function activate_venv () {
  if [[ ! -z "${VIRTUAL_ENV:-}" ]]; then
    echo "Virtualenv is active!"
    return 0
  fi

  echo "Init virtualenv"
  pip install --user virtualenv==20.24.6

  echo "Build virtualenv"
  NILLION_VENV=$(mktemp -d --suffix '-virtualenv')
  virtualenv -p python3 "$NILLION_VENV"

  echo "Activate virtualenv"
  source "$NILLION_VENV/bin/activate"

  echo "Virtualenv READY"
}

activate_venv
