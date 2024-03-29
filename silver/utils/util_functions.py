import json
import base64
import requests
from pymongo import MongoClient
import os
import logging

GOLD_URL = os.environ.get('GOLD_URL', 'http://gold:8080/')

def send_to_gold(data):
    print(base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8"), flush=True)
    pubsub_message = {
        "message": {
            "data": base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8"),
            "attributes": {},
            "messageId": "fake-message-id"
        },
        "subscription": "projects/fake-project/subscriptions/fake-subscription"
    }

    try:
        response = requests.post(GOLD_URL, json=pubsub_message)
        if response.status_code == 200:
            logging.info("Message sent successfully to Gold service.")
        else:
            logging.info(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.error(f"An error occurred while sending message to Gold service: {e}")
