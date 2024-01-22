import json
import base64
import requests
from pymongo import MongoClient

GOLD_URL = os.environ.get('GOLD_URL', 'http://gold:8080/')

def send_to_gold(data):
    # Construct the Pub/Sub message envelope and data payload
    pubsub_message = {
        "message": {
            "data": base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8"),
            "attributes": {},
            "messageId": "fake-message-id"
        },
        "subscription": "projects/fake-project/subscriptions/fake-subscription"
    }

    try:
        # Sending the constructed message
        response = requests.post(GOLD_URL, json=pubsub_message)
        if response.status_code == 200:
            print("Message sent successfully to Gold service.")
        else:
            print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"An error occurred while sending message to Gold service: {e}")
