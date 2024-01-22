from flask import Flask, request, jsonify
from pymongo import MongoClient
from utils.util_functions import write_to_db
import os
import json
import base64

app = Flask(__name__)

# MongoDB connection string
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://root:example@mongodb:27017/')
DB_NAME = 'reddit'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

@app.route('/insert', methods=['POST'])
def insert_data():
    envelope = request.json
    if not envelope:
        return jsonify({'error': 'No envelope provided'}), 400

    encoded_data = envelope.get('message', {}).get('data', '')
    if not encoded_data:
        return jsonify({'error': 'No data provided'}), 400

    # Decode the base64 encoded data
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    data = json.loads(decoded_data)

    # Insert decoded data into MongoDB
    result = write_to_db(data)

    # Return the MongoDB insert result
    return jsonify({'message': 'Data inserted'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))