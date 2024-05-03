### Run permissions examples (storing and retrieving permissioned secrets, revoking permissions)

Before running through examples, `./bootstrap-local-environment.sh` creates user keys for the secret writer and for the reader who the writer will allow to read the secret. Permissions examples are labeled 1-5:

1. The reader fetches their user id
2. The writer stores a secret and gives the reader retrieve permissions on the secret based on the reader's user id, resulting in a store id for the secret
3. The reader retrieves the secret with the store id
4. The writer revokes secret permissions by rewriting them
5. The reader tries to retrieve the secret, but no longer has access to it

To run through the example flow, simply run the python scripts in order. The output of a script will show you what to run next. Below gives the structure of the commands needed.

```shell
python3 01_fetch_reader_userid.py
python3 02_store_permissioned_secret.py --retriever_user_id {READER_USER_ID}
python3 03_retrieve_secret.py --store_id {STORE_ID}
python3 04_revoke_read_permissions.py --store_id {STORE_ID} --revoked_user_id {READER_USER_ID}
python3 05_test_revoked_permissions.py  --store_id {STORE_ID}
```
