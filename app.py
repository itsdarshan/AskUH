import flask
import os
from flask import send_from_directory, request
from kb_connector import read_cloud_csv, update_csv_content, sample_reload_document
from google.cloud import dialogflow_v2beta1
from google.cloud import storage
from creds import project_id as pid, knowledge_base_id as kid, \
    content_uri as link, display_name as dname, \
    bucket_name as bname, file_name as fname

app = flask.Flask(__name__)


def webhook(request):
    
    request_json = request.get_json()
    
    # retrieving questinos and answers from request
    question = request_json.get('queryResult').get('parameters').get('question')
    answer = request_json.get('queryResult').get('parameters').get('answer')
    print('Question: ', question)
    print('Answer: ', answer)

    storage_client = storage.Client(project='swift-catfish-369404')
    client = dialogflow_v2beta1.DocumentsClient()

    # performing read, update and reload on KB
    kb = read_cloud_csv(storage_client, bname, fname)
    update_csv_content(storage_client, kb, question, answer)
    sample_reload_document(client)

    return 'ok', 200
