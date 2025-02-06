from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from nada_dsl import *

# Load the document and split it into chunks


def nada_main():
    loader = TextLoader("payments.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(docs, embedding_function)
    print(docs[0].page_content) 
    vector = embedding_function.embed_query(docs[0].page_content)
    storage_party = Party(name=vector) 
    secret_vector = SecretInteger(Input(name="vector", party=storage_party))
    stored_vector = Output(secret_vector, "stored_vector", storage_party)

    return [stored_vector]

# Execute the nada_main function to store the vector 
stored_results = nada_main()
print(stored_results)

