import json
import base64
import pytest
from bson.objectid import ObjectId

def test_insert_data(client, mongo_mock):
    data = [
        {
            "subreddit_id": str(ObjectId()),
            "author_id": str(ObjectId()),
            "media_ids": [str(ObjectId()), str(ObjectId())],
            "content": "Example content"
        }
    ]
    encoded_data = base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')
    envelope = {
        "message": {
            "data": encoded_data
        }
    }

    # Set up the mock to simulate insertion
    mongo_mock.insert_many.return_value = type('obj', (object,), {'inserted_ids': [ObjectId() for _ in data]})

    response = client.post('/insert', json=envelope)
    assert response.status_code == 200
    assert 'Data inserted successfully' in response.json['message']

def test_insert_no_envelope(client):
    response = client.post('/insert', json={})
    assert response.status_code == 400
    assert 'No envelope provided' in response.json['error']

def test_insert_no_data(client):
    envelope = {"message": {}}
    response = client.post('/insert', json=envelope)
    assert response.status_code == 400
    assert 'No data provided' in response.json['error']

def test_insert_invalid_data(client, mongo_mock):
    data = {"invalid": "data"}
    encoded_data = base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')
    envelope = {
        "message": {
            "data": encoded_data
        }
    }

    mongo_mock.insert_many.side_effect = Exception('Insert failed')

    response = client.post('/insert', json=envelope)
    assert response.status_code == 500
