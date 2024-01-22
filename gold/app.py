from flask import Flask, request, jsonify
import os
from bson.objectid import ObjectId
from pymongo import MongoClient
import json
import base64

app = Flask(__name__)

MONGO_USER = os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'root')
MONGO_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD', 'rootpassword')
MONGO_HOST = os.environ.get('MONGO_HOST', 'mongodb_container')
MONGO_DB = os.environ.get('MONGO_DB')

mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:27017/"
client = MongoClient(mongo_uri)
db = client[MONGO_DB]

@app.route('/insert', methods=['POST'])
def insert_data():
    envelope = request.json
    if not envelope:
        return jsonify({'error': 'No envelope provided'}), 400

    encoded_data = envelope.get('message', {}).get('data', '')
    if not encoded_data:
        return jsonify({'error': 'No data provided'}), 400

    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    data = json.loads(decoded_data)

    for element in data:
        element['subreddit_id'] = ObjectId(element['subreddit_id'])
        element['author_id'] = ObjectId(element['author_id'])
        element['media_ids'] = [ObjectId(id_str) for id_str in element['media_ids']]

    try:
        result = db['posts'].insert_many(data)
        return jsonify({'message': 'Data inserted successfully', 'inserted_ids': str(result.inserted_ids)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))