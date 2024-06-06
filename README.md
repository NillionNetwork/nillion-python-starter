# Nillion Python Starter <a href="https://github.com/NillionNetwork/nillion-python-starter/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>

This is an EXPERIMENTAL PAYMENTS ENABLED BRANCH of python starter repo for building on the Nillion Network. In order to use this branch, you'll need the latest experimental version of the Nillion SDK, nada library, and python client library.

## Installing the latest experimental versions of Nillion

#### Prerequisites: Install the CLI Dependencies

The [`bootstrap-local-environment.sh`](./bootstrap-local-environment.sh) file uses `pidof` and `grep`.

- [Install `pidof`](https://command-not-found.com/pidof)
- [Install `grep`](https://command-not-found.com/grep)

### Setup

1.  Install the specific version of nillion with flags to also download nada and the python client at the same specific version by running

    ```bash
    nilup install {version} --nada-dsl --python-client
    ```

    This results in a message that shows you the downloaded paths to the versions of nada_dsl and the python client you’ll need to use, for example if I was downloading a version `vABCD`, I would see:

    ```bash
    Using pip to install /Users/steph/.nilup/sdks/vABCD/nada_dsl-0.1.0-py3-none-any.whl
    nada_dsl version vABCD installed
    Installing python client version vABCD
    Downloading vABCD/py_nillion_client-0.1.1-cp37-abi3-macosx_11_0_arm64.whl to /Users/steph/.nilup/sdks/vABCD/py_nillion_client-0.1.1-cp37-abi3-macosx_11_0_arm64.whl
    Using pip to install /Users/steph/.nilup/sdks/vABCD/py_nillion_client-0.1.1-cp37-abi3-macosx_11_0_arm64.whl
    python client version vABCD installed
    ```

    Use this message to figure out your local paths to the latest experimental versions of

    - python client path: `/Users/steph/.nilup/sdks/vABCD/py_nillion_client-0.1.1-cp37-abi3-macosx_11_0_arm64.whl`
    - nada path: `/Users/steph/.nilup/sdks/vABCD/py_nillion_client-0.1.1-cp37-abi3-macosx_11_0_arm64.whl`

2.  Set nillion version

```bash
nilup use {version}
```

3. Change directories into this branch of this repo

   ```
   cd nillion-python-starter
   git branch payments-flow-update
   git checkout payments-flow-update
   git pull origin payments-flow-update
   ```

4. Create venv

   ```bash
   bash ./create_venv.sh && source .venv/bin/activate
   ```

5. Manually install nada using the path printed by nilup installation in step 1

   ```bash
   python3 -m pip install {your/nada/path}
   ```

6. Manually install the Python client using the path printed by nilup installation in step 1

   ```bash
   python3 -m pip install {your/python/client/path}
   ```

7. Bootstrap local environment to connect to the nillion-devnet and add the configuration to your .env file

   ```bash
   ./bootstrap-local-environment.sh
   ```

8. Compile all programs

   Nada programs need to be compiled ahead of being stored. Compile all programs in the [programs](./programs/) folder with the script [`compile_programs.sh`](./compile_programs.sh):

   ```shell
   bash compile_programs.sh
   ```

   This generates a `programs-compiled` folder containing the compiled programs.

## Usage

After completing environment setup, then run the examples:

- To run multi party examples, go to the [multi party compute](examples_and_tutorials/core_concept_multi_party_compute) folder.

- To run single party examples, go to the [single party compute](examples_and_tutorials/core_concept_single_party_compute) folder.

- To run permissions examples (storing and retrieving permissioned secrets, revoking permissions, etc.), go to the [permissions](examples_and_tutorials/core_concept_permissions) folder.

## Store a Compiled Program

Store a compiled program in the network with this script:

```shell
bash store_program.sh {RELATIVE_COMPILED_PROGRAM_PATH}
```

To store the compiled [`addition_simple`](./programs/addition_simple.py) program you can run:

```shell
bash store_program.sh programs-compiled/addition_simple.nada.bin
```

Storing a program results in the stored `program_id`, the network's reference to the program. The `program_id` is the `{user_id}/{program_name}`.

## Testing

Most examples and tutorials within this repository can be tested. Docker is required to run the tests.

```shell
cd testing
bash run_tests.sh
```
