from flask import Flask, request, jsonify
import os
from pymongo import MongoClient
import json
import base64

app = Flask(__name__)

# Create a global MongoDB client
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://root:rootpassword@mongodb_container:27017/')
client = MongoClient(mongo_uri)
db = client['test']  # Adjust the database name as needed

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

    try:
        # Assuming 'data' is a list of documents to insert
        result = db['posts'].insert_many(data)  # Adjust the collection name as needed
        return jsonify({'message': 'Data inserted successfully', 'inserted_ids': str(result.inserted_ids)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))