import json
import requests
import base64

def process_jsonl_file(filepath):
    print(f'Processing file: {filepath}')
    batch = []
    batch_size = 50  # Number of lines to send at a time

    with open(filepath, 'r') as file:
        for line in file:
            # Convert each line to a dictionary and add to the batch
            try:
                data = json.loads(line.strip())  # Assuming each line is a valid JSON string
                batch.append({"data": data})
            except json.JSONDecodeError as e:
                print(f'Error decoding JSON from line: {e}')
                continue

            # Check if the batch size is reached
            if len(batch) >= batch_size:
                # Send the batch
                send_to_silver(batch)
                batch = []  # Reset the batch

        # Send any remaining lines in the batch
        if batch:
            send_to_silver(batch)

def send_to_silver(data):
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
    url = 'http://silver:8080/'

    try:
        # Sending the constructed message
        response = requests.post(url, json=pubsub_message)
        if response.status_code == 200:
            print("Message sent successfully to Silver service.")
        else:
            print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"An error occurred while sending message to Silver service: {e}")
