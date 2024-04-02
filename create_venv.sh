#!/usr/bin/env bash

function create_venv () {
  if [[ ! -z "${VIRTUAL_ENV:-}" ]]; then
    echo "Virtualenv is already active! Run 'deactivate' to deactivate the virtualenv."
    return 0
  fi

  echo "Creating virtualenv"
  python3 -m pip install --user virtualenv==20.24.6

  NILLION_VENV=".venv"
  mkdir -p "$NILLION_VENV"
  python3 -m virtualenv -p python3 "$NILLION_VENV"
  source "$NILLION_VENV/bin/activate"
  python3 -m pip install -r requirements.txt

  echo "Virtualenv: $NILLION_VENV"
  echo "Check the $NILLION_VENV/lib/python3.1X/site-packages folder to make sure you have py_nillion_client and nada_dsl packages"
  echo "📋 Copy and run the following command to activate your environment:"
  echo "source $NILLION_VENV/bin/activate"
}

create_venv
