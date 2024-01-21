import os
import zipfile
import requests
import zstandard as zstd
from flask import Flask, request, jsonify
import logging
import base64
from google.cloud import pubsub_v1

SILVER_URL = os.environ.get('SILVER_URL')

topic_name = 'my-topic'
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('fake-project', topic_name)

app = Flask(__name__)

GOOGLE_DRIVE_FILE_ID = os.environ.get('GOOGLE_DRIVE_FILE_ID')
DESTINATION_ZST_PATH = '/tmp/file.zst'
DECOMPRESSED_OUTPUT_PATH = '/tmp/decompressed_output.jsonl'

def process_jsonl_file(filepath):
    print(f'Processing file: {filepath}')
    with open(filepath, 'r') as file:
        for line in file:
            print(f'Processing line: {line}')
            data = line.encode('utf-8')
            try:
                publish_future = publisher.publish(topic_name, data)
                publish_future.result()  # Verify the publish succeeded
            except Exception as e:
                print(f'An error occurred: {e}')
    try:
        publish_message('hello world')
    except Exception as e:
        Exception(f'An error occurred reading file and publishing to pubsub: {e}')

def publish_message(data):
    # Data must be a bytestring
    try:
        data = data.encode("utf-8")
        future = publisher.publish(topic_path, data)
        print(f"Published {data} to {topic_path}.", flush=True)
    except Exception as e:
        print(f'An error occurred: {e}', flush=True)

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
        process_jsonl_file(DECOMPRESSED_OUTPUT_PATH)
    except Exception as e:
        print(f'Error with processing: {e}')
        return jsonify({"status": "failed", "message": f"Error with jsonl: {e}"})
    
    return jsonify({"status": "completed"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
