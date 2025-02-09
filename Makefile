.PHONY: all clean install dev venv deps help nilup activate devnet example check_venv check_nillion

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
CONFIG_DIR := $(HOME)/.config/nillion
SHELL := /bin/bash
QUICK_START_DIR := $(shell pwd)/quickstart_complete/nada_quickstart_programs
SEPARATOR := "=================================================="

ifeq ($(OS),Windows_NT)
    VENV_ACTIVATE := $(VENV)/Scripts/activate
else
    VENV_ACTIVATE := $(VENV)/bin/activate
endif

.DEFAULT_GOAL := help

help:
	@echo $(SEPARATOR)
	@echo "  Usage:"
	@echo
	@echo "    make nilup      Install nilup and Nillion SDK"
	@echo "    make install    Install all dependencies and setup environment (requires nilup)"
	@echo "    make dev        Setup development environment"
	@echo "    make clean      Remove virtual environment and cached files"
	@echo "    make deps       Install/update dependencies only"
	@echo "    make activate   Activate the virtual environment"
	@echo "    make devnet     Start the Nillion devnet"
	@echo "    make example    Build the quickstart example"
	@echo "    make help       Show this help message"
	@echo $(SEPARATOR)

check_venv:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo $(SEPARATOR); \
		echo "  Error: Virtual environment is not activated"; \
		echo; \
		echo "  Please run 'make activate' and follow the instructions"; \
		echo $(SEPARATOR); \
		exit 1; \
	fi

check_nillion:
	@if ! command -v nillion > /dev/null; then \
		echo $(SEPARATOR); \
		echo "  Error: nillion command not found"; \
		echo; \
		echo "  Please run 'make install' first to set up the environment"; \
		echo $(SEPARATOR); \
		exit 1; \
	fi

activate:
	@if [ ! -d "$(VENV)" ]; then \
		echo $(SEPARATOR); \
		echo "  Error: Virtual environment not found"; \
		echo; \
		echo "  Please run 'make install' first to set up the environment"; \
		echo $(SEPARATOR); \
		exit 1; \
	fi
	@echo $(SEPARATOR)
	@echo "  To activate the virtual environment, run:"
	@echo
	@echo "    source $(VENV_ACTIVATE)"
	@echo $(SEPARATOR)

nilup:
	@echo $(SEPARATOR)
	@if ! command -v nilup > /dev/null; then \
		echo "  Installing nilup..."; \
		curl -s https://nilup.nilogy.xyz/install.sh | bash; \
		echo; \
		echo "  Please close and reopen your terminal, then run 'make install'"; \
		echo $(SEPARATOR); \
		exit 1; \
	fi
	@echo "  nilup is already installed"
	@echo $(SEPARATOR)

	
$(VENV):
	virtualenv $(VENV)
	$(PIP) install --upgrade pip

deps: $(VENV)
	$(PIP) install -r requirements.txt

$(CONFIG_DIR):
	mkdir -p $(CONFIG_DIR)

install: $(VENV) deps $(CONFIG_DIR)
	@if ! command -v nilup > /dev/null; then \
		echo $(SEPARATOR); \
		echo "  Error: nilup not found. Please run 'make nilup' first"; \
		echo $(SEPARATOR); \
		exit 1; \
	fi
	@if ! command -v nillion > /dev/null; then \
		nilup install latest; \
		nilup use latest; \
	fi

devnet: check_venv check_nillion
	nillion-devnet

dev: install
	@echo $(SEPARATOR)
	@echo "  Development environment ready"
	@echo
	@echo "  Run 'make activate' to activate the virtual environment"
	@echo "  Run 'make devnet' in a separate terminal to start the devnet"
	@echo $(SEPARATOR)

example: check_venv check_nillion
	@if [ ! -d "$(QUICK_START_DIR)" ]; then \
		echo $(SEPARATOR); \
		echo "  Error: Quickstart directory not found at $(QUICK_START_DIR)"; \
		echo; \
		echo "  Please ensure you have the correct project structure"; \
		echo $(SEPARATOR); \
		exit 1; \
	fi
	cd $(QUICK_START_DIR) && nada build

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete