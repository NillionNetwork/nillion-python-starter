# Nillion Python Starter <a href="https://github.com/nillion-oss/nillion-python-starter/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>


This is a python starter repo for building on the Nillion Network. Complete environment setup, then run the examples:

- To run multi party examples, go to the [client_multi_party_compute](./client_multi_party_compute) folder.

- To run single party examples, go to the [client_single_party_compute](./client_single_party_compute) folder.

- To run permissions examples (storing and retrieving permissioned secrets, revoking permissions, etc.), go to the [permissions](./permissions) folder.

### Prerequisites: Install the CLI Dependencies

The `run-local-cluster` tool spins up `anvil` under the hood, so you need to have `foundry` installed. The [`bootstrap-local-environment.sh`](./bootstrap-local-environment.sh) file uses `pidof` and `grep`.

- [Install `foundry`](https://book.getfoundry.sh/getting-started/installation)
- [Install `pidof`](https://command-not-found.com/pidof)
- [Install `grep`](https://command-not-found.com/grep)

## Environment Setup

1. Create a `.env` file by copying the sample:

    ```shell
    cp .env.sample .env
    ```

2. Update the following variables within the `.env` file: `NILLION_WHL_ROOT`, `NILLION_SDK_ROOT`, `NILLION_PYCLIENT_WHL_FILE_NAME`.

3. Activate the virtual environment (`.venv`) and install dependencies

    ```shell
    ./activate_venv.sh
    source .venv/bin/activate
    ```

    Run the [`bootstrap-local-environment.sh`](./bootstrap-local-environment.sh) script to `run-local-cluster`, generate keys, and get bootnodes, cluster, and payment info:

    ```shell
    ./bootstrap-local-environment.sh
    ```

4. Check `.env` file - keys, bootnodes, cluster, and payment info should now be present. If you want to run against a local cluster, use this configuration. Otherwise, replace values with testnet bootnodes, cluster, and payment info.

5. Look through the [programs](./programs/) folder to see examples of Nada programs.

## Compiling Programs

Nada programs need to be compiled ahead of being stored. Compile all programs in the [programs](./programs/) folder with the script [`compile_programs.sh`](./compile_programs.sh):

```shell
./compile_programs.sh
```

This generates a `programs-compiled` folder containing the compiled programs.

## Store a Compiled Program

Store a compiled program in the network with this script:

```shell
./store_program.sh {RELATIVE_COMPILED_PROGRAM_PATH}
```

To store the compiled [`addition_simple`](./programs/addition_simple.py) program you can run:

```shell
./store_program.sh programs-compiled/addition_simple.nada.bin
```

Storing a program results in the stored `program_id`, the network's reference to the program. The `program_id` is the `{user_id}/{program_name}`.
