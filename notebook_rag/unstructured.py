import os
from dotenv import load_dotenv

load_dotenv()

UNSTRUCTURED_API_KEY = os.getenv("UNSTRUCTURED_API_KEY")
UNSTRUCTURED_API_URL = os.getenv("UNSTRUCTURED_API_URL")

import os, json
import unstructured_client
from unstructured_client.models import operations, shared

## Create a class for Ingestion

def create_client():
    return unstructured_client.UnstructuredClient(
    api_key_auth=UNSTRUCTURED_API_KEY,
    server_url=UNSTRUCTURED_API_URL,
)

def ingest_document(client, file_upload_dir, output_dir, workspace, filename, new_json_filename):

    filepath = f'{file_upload_dir}/{workspace}/{filename}'

    try:
        with open(filepath, "rb") as f:
            data = f.read()
    except Exception as e:
        return f'{workspace}:{filename} could not be read...ingestion failed'

    req = operations.PartitionRequest(
        partition_parameters=shared.PartitionParameters(
            files=shared.Files(
                content=data,
                file_name=filename,
            ),
            strategy=shared.Strategy.HI_RES,
            languages=['eng'],
            split_pdf_page=True,            # If True, splits the PDF file into smaller chunks of pages.
            split_pdf_allow_failed=True,    # If True, the partitioning continues even if some pages fail.
            split_pdf_concurrency_level=15  # Set the number of concurrent request to the maximum value: 15.
        ),
    )

    try:
        res = client.general.partition(request=req)
        element_dicts = [element for element in res.elements]

        json_elements = json.dumps(element_dicts, indent=2)

        output_dir = f'{output_dir}/{workspace}/'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(output_dir + new_json_filename, "w") as json_file:
            json_file.write(json_elements)

    except Exception as e:
        print(e)

    return f'Ingestion of {workspace}:{filename} completed'

