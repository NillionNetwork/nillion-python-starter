# Permissions python examples

Before running through permissions examples, `./bootstrap-local-environment.sh` creates user keys for the secret writer and for the reader who the writer will allow to read the secret. Permissions examples are labeled 1-5:

1. The reader fetches their user id
2. The writer stores a secret and gives the reader retrieve permissions on the secret based on the reader's user id, resulting in a store id for the secret
3. The reader retrieves the secret with the store id
4. The writer revokes secret permissions by rewriting them
5. The reader tries to retrieve the secret, but no longer has access to it

## Getting started with permissions examples

### Pre-req: install cli dependencies

The bootstrap-local-environment.sh file uses pidof and grep.

- [Install pidof](https://command-not-found.com/pidof)
- [Install grep](https://command-not-found.com/grep)

### Running examples

1. Create a .env file by copying the sample

`cp .env.sample .env`

2. Update variables within the .env: NILLION_WHL_ROOT, NILLION_SDK_ROOT, NILLION_PYCLIENT_WHL_FILE_NAME

3. Activate environment, install requirements, and run bootstrap-local-environment.sh to run-local-cluster, generate keys, and get bootnodes, cluster, and payment info

```shell
source ./activate_venv.sh
pip install -r requirements.txt
./bootstrap-local-environment.sh
```

4. Check .env file - keys, bootnodes, cluster, and payment info should now be present.

5. Run permissions examples

```shell
cd permissions
python3 01-fetch-reader-userid.py
python3 02-store-permissioned-secret.py --retriever_user_id {READER_USER_ID}
python3 03-retrieve-secret.py --store_id {STORE_ID}
python3 04-revoke-read-permissions.py --store_id {STORE_ID} --revoked_user_id {READER_USER_ID}
python3 05-test-revoked-permissions  --store_id {STORE_ID}
```

# Running permissions example in Docker

```shell
cd permissions
docker compose run demo
```
