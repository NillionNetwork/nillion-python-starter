#!/usr/bin/env bash

set -e

NILLION_VENV="nillion-venv"

export PYENV_ROOT="$HOME/.pyenv"

if [ ! -d "$PYENV_ROOT" ]; then
    curl https://pyenv.run | bash > /dev/null
fi

set +e
if ! command -v pyenv &>/dev/null; then
  export PATH="${PYENV_ROOT}/bin:${PATH}"
fi
set -e

function activate_venv() {
    echo Initializing pyenv
    eval "$(pyenv init -)"

    echo Activating "$NILLION_VENV"
    pyenv activate "$NILLION_VENV"
}

function deactivate_venv() {
    echo Deactivating "$NILLION_VENV"
    pyenv deactivate "$NILLION_VENV"
}

activate_venv

# Deactivate on exit
trap deactivate_venv EXIT
