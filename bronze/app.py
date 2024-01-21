import os
import zipfile
import requests
import zstandard as zstd
from flask import Flask, request, jsonify
import logging
import base64
from google.cloud import pubsub_v1
from utils.util_functions import process_jsonl_file
from constants import (
    GOOGLE_DRIVE_FILE_ID, 
    DESTINATION_ZST_PATH, 
    DECOMPRESSED_OUTPUT_PATH, 
    topic_name
)

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('fake-project', topic_name)

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({"status": "healthy"})


@app.route('/process-zst', methods=['POST'])
def process_zst_file():
    try:
        download_url = f'https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}&export=download'
        
        # Download the file from Google Drive
        response = requests.get(download_url)
    except Exception as e:
        return jsonify({"status": "failed", "message": f"Error with requests: {e}"})
    
    try:
        with open(DESTINATION_ZST_PATH, 'wb') as file:
            file.write(response.content)
        
        # Decompress the Zstandard file
        with open(DESTINATION_ZST_PATH, 'rb') as compressed:
            with open(DECOMPRESSED_OUTPUT_PATH, 'wb') as decompressed:
                dctx = zstd.ZstdDecompressor()
                dctx.copy_stream(compressed, decompressed)
    except Exception as e:
        return jsonify({"status": "failed", "message": f"Error with decompression: {e}"})
    
    try:
        process_jsonl_file(DECOMPRESSED_OUTPUT_PATH, publisher, topic_path)
    except Exception as e:
        print(f'Error with processing: {e}')
        return jsonify({"status": "failed", "message": f"Error with jsonl: {e}"})
    
    return jsonify({"status": "completed"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
