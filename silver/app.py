import base64
import os
import json
from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from utils.util_functions import translate_schema

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
    if not envelope or not isinstance(envelope, dict) or 'message' not in envelope:
        msg = 'Invalid Pub/Sub message format'
        print(f'error: {msg}')
        return f'Bad Request: {msg}', 400

    pubsub_message = envelope['message']

    # Decode the Pub/Sub message
    message_data = base64.b64decode(pubsub_message['data']).decode('utf-8').strip()

    # Process the JSON objects in the message data
    data_to_insert = []
    try:
        json_data = json.loads(message_data)
        for data_entry in json_data:
            data_to_insert.append(translate_schema(data_entry))
        
        # insert into mongodb
    except Exception as e:
        print(f'error: {e}')
        return jsonify({"status": "failed", "message": str(e)}), 500

    return jsonify({"status": "completed"}), 200    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
