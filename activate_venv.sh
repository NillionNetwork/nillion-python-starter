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
      
  else
      echo "$NILLION_VENV does not exist, creating virtual environment."
      mkdir "$NILLION_VENV"
      virtualenv -p python3.11 "$NILLION_VENV"
  fi

  source "$NILLION_VENV/bin/activate"
  source ./install-nillion.sh
  echo "Virtualenv: $NILLION_VENV"
  echo "Check the $NILLION_VENV/lib/python3.11/site-packages folder to make sure you have py_nillion_client and nada_dsl packages"
  echo "📋 Copy and run the following command to activate your environment:"
  echo "source .venv/bin/activate"
}

activate_venv