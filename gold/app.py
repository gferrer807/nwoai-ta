from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection string
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://root:example@mongodb:27017/')
DB_NAME = 'reddit'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Assuming data is for posts collection
    result = db.posts.insert_one(data)
    return jsonify({'message': 'Data inserted', 'id': str(result.inserted_id)}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))