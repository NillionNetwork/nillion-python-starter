# Voting tutorial

This tutorial aims to introduce you to the features of PyNada embedded DSL through the use of voting systems. We'll start simple and gradually increase the complexity of the programs to show you some interesting techniques.

Additionally, we've provided two sets of Python scripts for you to explore the flow of a voting system running in `devnet-nillion`:

1. Single File: One script emulates the behavior of all parties.
2. Multiple Files: Each party runs in its own separate script.

In a real-world scenario, the roles should be distributed across multiple machines.

## Tutorial

Please go to the [tutorial page](tutorial.md) to dive deeper into PyNada.

## Setup

Before running the example, [follow the repo README](../../README.md) to install cli dependencies, complete environment setup, and activate your .venv environment.

## Single file example

In the single file version, the different roles are played by a single entity (`general_client`). The script has the following flow:

    1. Parties initialization.
    2. Owner stores a program.
    3. (Real environment:) Owner sends the program ID to all voters.
    4. Voters store votes:
        4.1 Bind voter to party in the program
        4.2 Set compute permission to owner
    5. (Real environment:) Voters send their their party IDs and store IDs to the owner.
    6. Owner compute voting system using votes from voters.

Also, we present a function [`digest_plurality_vote_robust_result()`](digest_result.py) that digests the result output by the [voting_dishonest_robust_6.py](../../programs/voting_dishonest_robust_6.py).

### Run

Run the command to start the example and follow the steps described:
```bash
python3 client_voting.py
```

## Multiple files example

In this voting example, we maintain the same structure as in previous multiparty computation examples:

- Alice assumes the role of the owner and acts as voter 0.
- Bob serves as voter 1.
- Charlie takes on the role of voter 2.

Furthermore, the voters will cast their votes for two candidates: Dave and Emma.

### Step 1

- Alice creates and stores program in the network
- Alice shares her user id and the resulting program id with Bob and Charlie

Run the command to perform step 1.

```bash
python3 01_store_secret_party1.py
```

### Step 2

- Bob and Charlie store their VOTES in the network as secrets. Each secret is stored with
  - **bindings** to the voting program id.
  - **permissions** so Alice (the owner) can compute using the secret.
- Bob and Charlie each share their `party_id` and secret `store_id` with Alice.

The script will provide the command to perform step 2.

```bash
python3 02_store_secret_party_n.py --user_id_1 {user_id} --program_id {program_id}
```

### Step 3

- Alice runs voting program computation using Bob and Charlie's secret votes. She provides her own vote as a secret at computation time.
- Alice receives the output result of the program.

The script will provide the command to perform step 3.

```bash
python3 03_multi_party_compute.py --program_id {program_id} --party_ids_to_store_ids {party_ids_to_store_ids}
```

Also, we present a function [`digest_plurality_vote_robust_result()`](digest_result.py) that digests the result output by the [voting_dishonest_robust_6.py](../../programs/voting_dishonest_robust_6.py).
