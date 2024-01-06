#!/usr/bin/env bash

function deactivate_venv() {
    echo "Deactivating virtualenv"
    deactivate
}

function activate_venv () {
  if [[ ! -z "${VIRTUAL_ENV:-}" ]]; then
    echo "Virtualenv is already active at $NILLION_VENV! Run 'deactivate' to deactivate the virtualenv."
    return 0
  fi

  echo "Init virtualenv"
  pip install --user virtualenv==20.24.6

  echo "Check and build virtualenv"
  NILLION_VENV=".venv"

  # Check if the .venv directory exists
  if [ -d "$NILLION_VENV" ]; then
      echo "$NILLION_VENV exists, activating virtual environment."
      source "$NILLION_VENV/bin/activate"
  else
      echo "$NILLION_VENV does not exist, creating virtual environment."
      mkdir "$NILLION_VENV"
      virtualenv -p python3 "$NILLION_VENV"
      source "$NILLION_VENV/bin/activate"
  fi

  echo "Virtualenv ready: $NILLION_VENV"
}

activate_venv
