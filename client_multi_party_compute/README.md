# Multi Party Example

This is an example of multi party compute, computation involving secret inputs from multiple parties.

## Assumptions

The 3-part Multi Party example assumes there is a stored program that meets the following criteria:

- there are exactly 2 parties
- each party contributes secret inputs of type SecretInteger, and each party stores at least one secret an input
- the 2nd party gives the 1st party permission to compute on the 2nd party's secret
- the 1st party runs compute
- the 1st party reads the output

## Run the example

1. Set up requirements following the repo README to populate the .env file with environment variables.

2. Follow README instructions to compile and store a program that meets the above assumptions. Take note of the resulting program_id. Here are some programs that meet the multi party example program assumptions:

- addition_simple_multi_party.nada.bin
- circuit_simple_multi_party.nada.bin
- complex_operation_mix
- greater_or_equal_than
- greater_than
- import_file
- less_or_equal_than
- less_than
- multiplication_simple_multi_party.nada.bin
- single_addition_multi_party.nada.bin
- subtraction_simple_multi_party.nada.bin
- subtraction_simple_neg_multi_party.nada.bin
- reuse_simple_1_multi_party.nada.bin
- reuse_simple_sub_multi_party.nada.bin

For example before running addition_simple_multi_party.py, compile all programs and store addition_simple_multi_party.nada.bin in the network.

```bash
cd ..
./compile_programs.sh
./store_program.sh programs-compiled/addition_simple_multi_party.nada.bin
```

3. Update values in config.py to set the stored program_id, party names, secret names, and secret values.

4. Start the 3 part example by running

```bash
python3 01_store_secret_party1.py
```

5. Follow the cli directions to run part 2 and 3 of the example.
