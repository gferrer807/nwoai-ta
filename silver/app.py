import base64
import os
import json
from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from utils.util_functions import translate_schema, send_to_gold

app = Flask(__name__)

@app.route('/_ah/warmup')
def warmup():
    # Warmup requests are used in Cloud Run to initialize the instance
    return '', 200, {}

@app.route('/healthz', methods=['GET'])
def health_check():
    # Health check endpoint for Cloud Run
    return jsonify({"status": "healthy"}), 200

@app.route('/', methods=['POST'])
def process_pubsub_message():
    envelope = request.get_json()
    if not envelope or not 'message' in envelope or not 'data' in envelope['message']:
        msg = 'Invalid Pub/Sub message format'
        print(f'error: {msg}')
        return f'Bad Request: {msg}', 400

    pubsub_message = envelope['message']

    # Decode the Pub/Sub message data from base64
    message_data_encoded = pubsub_message['data']
    message_data_json = base64.b64decode(message_data_encoded).decode('utf-8')

    # Parse the JSON string to a Python object (dict or list)
    try:
        message_data = json.loads(message_data_json)
    except json.JSONDecodeError as e:
        return jsonify({'error': 'Decoding JSON failed', 'detail': str(e)}), 400

    # At this point, message_data is a Python object (dict or list) that you can work with
    # Example: print or process the data
    # print(message_data[0])

    # Process the JSON objects in the message data
    data_to_insert = []
    try:
        for data_entry in message_data:
            data_to_insert.append(translate_schema(data_entry))

        # insert into mongodb
        send_to_gold(data_to_insert)
    except Exception as e:
        print(f'error: {e}')
        return jsonify({"status": "failed", "message": str(e)}), 500

    return jsonify({"status": "completed"}), 200    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
