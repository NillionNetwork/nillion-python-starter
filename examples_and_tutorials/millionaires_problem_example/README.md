# MPC Millionaires Problem Example

In our version of the [Millionaires Problem](https://docs.nillion.com/multi-party-computation#classic-scenario-the-millionaires-problem), three friends, Alice, Bob & Charlie finish lunch and decide that the richest friend should pay the bill.

They want to figure out who has the highest salary without telling each other how much they earn.

Alice suggests that this is the perfect opportunity for the friends to use Nillion for blind computation on high value data to determine who should pay for lunch. She offers to create a millionaires problem program, compile it, and store it in Nillion so that the friends can run multi party blind computation to figure out who should pay for lunch.

- Alice's millionaires program in NADA: [../../programs/millionaires.py](https://github.com/NillionNetwork/nillion-python-starter/blob/main/programs/millionaires.py)
- Compiled program: [./millionaires.nada.bin](https://github.com/NillionNetwork/nillion-python-starter/blob/main/millionaires_problem_example/millionaires.nada.bin)

## Setup

Before running the example, [follow the repo README](https://github.com/NillionNetwork/nillion-python-starter/blob/main/README.md) to install cli dependencies, complete environment setup, and activate your .venv environment.

## Run the example

### Step 1

- Alice creates and stores program in the network
- Alice shares her user id and the resulting program id with Bob and Charlie

Run the command to perform step 1.

```bash
python3 01_store_secret_party1.py
```

### Step 2

- Bob and Charlie store their salaries in the network as secrets. Each secret is stored with
  - **bindings** to the millionaires program id
  - **permissions** so Alice can compute using the secret
- Bob and Charlie each share their party_id and secret store_id with Alice.

The script will provide the command to perform step 2.

```bash
python3 02_store_secret_party_n.py --user_id_1 {user_id} --program_id {program_id}
```

### Step 3

- Alice runs millionaires program computation using Bob and Charlie's secret salaries. She provides her own salary as a secret at computation time.
- Alice receives the output result of the program, and the friends know that Charlie should pay for lunch.

The script will provide the command to perform step 3.

```bash
python3 03_multi_party_compute.py --program_id {program_id} --party_ids_to_store_ids {party_ids_to_store_ids}
```
