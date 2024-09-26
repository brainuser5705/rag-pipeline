from langchain_openai import OpenAIEmbeddings
import unstructured
import qdrant
import os
import json
import time


embedding_model = OpenAIEmbeddings(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studios",
    check_embedding_ctx_length=False
)


FILE_UPLOAD_DIR = '/mnt/c/Users/codeu/Documents/afrl/rag-system/data'
OUTPUT_FILE_DIR = "/mnt/c/Users/codeu/Documents/afrl/rag-system/output"


def upload_files(files, job_queue):

    while True:
        workspace_name = input("What would you like to name your collection of documents?")
        workspace_path = f'{FILE_UPLOAD_DIR}/{workspace_name}/'
        if not os.path.exists(workspace_path):
            os.makedirs(workspace_path)
            break
        print(f'Workspace {workspace_name} already exists. Choose a different name.')
    
    for uploaded_file in files:
        file_name = uploaded_file['name']
        with open(workspace_path + file_name, 'wb') as new_file:
            new_file.write(uploaded_file['content'])

            job_queue.enqueue(process_file, workspace_name, file_name)
            time.sleep(2)
            print(f'Finish processing for {file_name} in {workspace_name}')


def process_file(workspace_name, filename):

    new_json_filename = os.path.splitext(filename)[0] + '.json'

    # Unstructured
    client = unstructured.create_client()
    unstructured.ingest_document(client, FILE_UPLOAD_DIR , OUTPUT_FILE_DIR, workspace_name, filename, new_json_filename)
    
    # Embedding
    chunks = []
    file = open(f'{OUTPUT_FILE_DIR}/{workspace_name}/{new_json_filename}')
    file_json = json.load(file)
    for chunk in file_json:
        embedding = embedding_model.embed_query(chunk['text'])
        chunk['embedding'] = embedding
        chunks.append(chunk)

    # Qdrant
    qdrant_client = qdrant.create_qdrant_client()
    qdrant.create_collection(qdrant_client, workspace_name)
    for chunk in chunks:
        qdrant.insert_qdrant_point(qdrant_client, workspace_name, chunk)