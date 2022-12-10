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


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    question = req.get('queryResult').get('parameters').get('question')
    answer = req.get('queryResult').get('parameters').get('answer')
    print('Question: ', question)
    print('Answer: ', answer)

    storage_client = storage.Client(project='swift-catfish-369404')
    client = dialogflow_v2beta1.DocumentsClient()

    kb = read_cloud_csv(storage_client, bname, fname)
    update_csv_content(storage_client, kb, question, answer)
    sample_reload_document(client)

    return 'OK', 200
    # return {
    #     'fulfillmentMessages': 'Your Question has been updated.'
    # }


if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.run()
