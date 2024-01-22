from flask import Flask, request, jsonify
import os
from utils.database_utils import prepare_and_insert_posts
import json
import base64


app = Flask(__name__)

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

    success, message = prepare_and_insert_posts(data)

    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))