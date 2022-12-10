import pandas as pd
from creds import project_id as pid, knowledge_base_id as kid, \
    content_uri as link, display_name as dname, \
    bucket_name as bname, file_name as fname
import csv
from google.cloud import dialogflow_v2beta1
from google.cloud import storage
from io import StringIO
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "swift-catfish-369404-04f8157d45c7.json"


def read_cloud_csv(client, bucket_name, file_name):
    # read cloud bucket for knowledge base csv
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('KB/' + file_name)
    blob = blob.download_as_string()
    blob = blob.decode('utf-8')

    # transform bytes to string here
    blob = StringIO(blob)
    # then use csv library to read the content
    csv_data = pd.read_csv(blob, header=None)

    return csv_data


def update_csv_content(client, csv_data, que, ans):
    # updating csv file with new data
    csv_data.loc[len(csv_data.index)] = [que, ans]

    bucket = client.bucket(bname)
    blob = bucket.blob('KB/' + fname)
    content = csv_data.to_csv(index=False, header=None)
    # uploading csv file back to cloud bucket
    blob.upload_from_string(content, 'text/csv')
    blob.reload(projection='full', client=client)

    print(
        f"File {fname} uploaded to cloud."
    )


def sample_reload_document(client):

    # Initialize request argument(s)
    request = dialogflow_v2beta1.ReloadDocumentRequest(
        name="projects/swift-catfish-369404/knowledgeBases/MTExMDE2OTQ2ODg2MTkzOTcxMjA/documents/MjQ2Mzk0NTYzNDQ2MjMwMjIwOA"
    )

    # Make the request
    operation = client.reload_document(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)


storage_client = storage.Client(project='swift-catfish-369404')
client = dialogflow_v2beta1.DocumentsClient()