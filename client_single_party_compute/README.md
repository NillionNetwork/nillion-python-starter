# Single Party Compute Examples

These compute examples only involve one party.

## Run an example

1. Set up requirements following the repo README to populate the .env file with environment variables.

2. Follow README instructions to compile and store the program of the same name as the file

For example before running addition_simple.py, compile all programs and store addition_simple.nada.bin in the network.

```bash
cd ..
./compile_programs.sh
./store_program.sh programs-compiled/addition_simple.nada.bin
```

3. Run the python example

```bash
python3 addition_simple.py
```
