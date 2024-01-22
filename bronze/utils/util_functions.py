import json
import requests
import base64
from constants import SILVER_URL
import logging

def process_jsonl_file(filepath):
    print(f'Processing file: {filepath}')
    batch = []
    batch_size = 50

    with open(filepath, 'r') as file:
        for line in file:
            try:
                data = json.loads(line.strip())
                batch.append({"data": data})
            except json.JSONDecodeError as e:
                logging.error(f'Error decoding JSON from line: {e}')
                continue

            if len(batch) >= batch_size:
                send_to_silver(batch)
                batch = []

        # Send any remaining lines in the batch
        if batch:
            send_to_silver(batch)

def send_to_silver(data):
    pubsub_message = {
        "message": {
            "data": base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8"),
            "attributes": {},
            "messageId": "fake-message-id"
        },
        "subscription": "projects/fake-project/subscriptions/fake-subscription"
    }
    
    url = SILVER_URL

    try:
        response = requests.post(url, json=pubsub_message)
        if response.status_code == 200:
            logging.info("Message sent successfully to Silver service.")
        else:
            logging.info(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.error(f"An error occurred while sending message to Silver service: {e}")
