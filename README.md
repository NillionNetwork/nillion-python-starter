# Nillion Python Starter <a href="https://github.com/NillionNetwork/nillion-python-starter/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>

Welcome to the start of your Nillion developer journey.

This repo corresponds to the Nillion Python quickstart. To get started with Nillion head over to the [Python QuickStart docs](https://docs.nillion.com/python-quickstart) and follow the quickstart guide. 

## Quick Setup

First, make sure that you have `virtualenv` and `make` installed. if not, installed them for your OS.

And then:
```bash
# Install nilup (Nillion SDK manager)
make nilup

# Install dependencies and setup development environment
make dev
```
After setup is complete, follow the displayed instructions to start developing with Nillion.

To build the quickstart example, run:
```bash
make example
``` 

## Available Commands
To see all available commands, run
```bash
make help
```

## Manual Setup

If you prefer to set up manually, head over to the [Python QuickStart docs](https://docs.nillion.com/python-quickstart) and follow the instructions.


## Examples

For more python examples, check out https://github.com/NillionNetwork/python-examples which contains the following:
- core_concept_multi_party_compute
- core_concept_permissions
- core_concept_single_party_compute
- core_concept_store_and_retrieve_secrets
- millionaires_problem_example
- nada_programs
- voting_tutorial
