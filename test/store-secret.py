from pdb import set_trace as bp
import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.nillion_client_helper import create_nillion_client

load_dotenv()



async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    writer_userkey_path = os.getenv("NILLION_WRITERKEY_PATH")
    writer_userkey = nillion.UserKey.from_file(writer_userkey_path)

    # Writer Nillion client
    writer = create_nillion_client(writer_userkey)
    writer_user_id = writer.user_id()

    # Writer gives themself default permissions
    permissions = nillion.Permissions.default_for_user(writer_user_id)
    # Writer gives the reader permission to read/retrieve secret

    retriever_user_id=writer_user_id
    permissions.add_retrieve_permissions(set([retriever_user_id]))

    program_name = "addition_simple"
    program_id = f"{writer_user_id}/{program_name}"

    compute_permissions = {
        retriever_user_id: {program_id},
        # writer_user_id: {program_id},
    }
    
    permissions.add_compute_permissions(compute_permissions)

    test_read_writer = permissions.is_retrieve_allowed(writer_user_id)
    print("read allowed for writer", test_read_writer)

    test_read_retriever = permissions.is_retrieve_allowed(retriever_user_id)
    print("read allowed for retriever", test_read_retriever)
    
    test_compute_writer = permissions.is_compute_allowed(writer_user_id, program_id)
    print("compute allowed for writer", test_compute_writer)

    test_compute_retriever = permissions.is_compute_allowed(retriever_user_id, program_id)
    print("compute allowed for retriever", test_compute_retriever)

    secret_name_1 = "my_int1"
    secret_1 = nillion.SecretInteger(10)

    # secret_name_2 = "my_int2"
    # secret_2 = nillion.SecretInteger(32)
    secrets_object = nillion.Secrets({
        secret_name_1: secret_1, 
        # secret_name_2: secret_2
    })


    writer_party_name = "Party1"
    
    secret_program_bindings = nillion.ProgramBindings(program_id)
    secret_program_bindings.add_input_party(writer_party_name, retriever_user_id)
    secret_program_bindings.add_output_party(writer_party_name, retriever_user_id)
    print(secret_program_bindings)

    # Writer stores the permissioned secret, resulting in the secret's store id
    print(f"ℹ️  Storing permissioned secret: {secrets_object}")
    store_id = await writer.store_secrets(
        cluster_id, secret_program_bindings, secrets_object, permissions
    )

    print("ℹ️ STORE ID:", store_id)
    print("\n\nRun the following command to retrieve the secret by store id as the reader")


asyncio.run(main())
