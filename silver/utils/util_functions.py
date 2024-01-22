import json
import base64
import requests

GOLD_URL = 'http://gold:8080/'

def translate_schema(raw_data):
    data = raw_data['data']
    try:
        id = data['id']
    except Exception as e:
        id = data['data']['id']
    return {
        'id': id,
    }

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
    
    # URL of the Silver service, using HTTP and the correct port
    url = GOLD_URL

    try:
        # Sending the constructed message
        response = requests.post(url, json=pubsub_message)
        if response.status_code == 200:
            print("Message sent successfully to Silver service.")
        else:
            print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"An error occurred while sending message to Silver service: {e}")
