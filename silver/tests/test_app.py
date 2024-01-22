import json
import base64
from bson.objectid import ObjectId

def test_warmup(client):
    response = client.get('/_ah/warmup')
    assert response.status_code == 200

def test_health_check(client):
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_process_pubsub_message_valid(client, pubsub_message_data, mongo_mock, gold_service_mock):
    # gold_service_mock is now an argument, ensuring it's applied before the request
    response = client.post('/', json=pubsub_message_data)
    assert response.status_code == 200
    assert response.json == {"status": "completed"}
    gold_service_mock.assert_called_once()

def test_process_pubsub_message_invalid_format(client):
    invalid_message = {'invalid': 'data'}
    response = client.post('/', json=invalid_message)
    assert response.status_code == 400
    assert 'Invalid Pub/Sub message format' in response.data.decode('utf-8')

def test_process_pubsub_message_invalid_data(client, gold_service_mock):
    invalid_data = {
        'message': {
            'data': base64.b64encode('invalid data'.encode('utf-8')).decode('utf-8'),
            'attributes': {},
            'messageId': 'test-message-id'
        },
        'subscription': 'test-subscription'
    }
    response = client.post('/', json=invalid_data)
    assert response.status_code == 400
    assert 'Decoding JSON failed' in response.json['error']
    gold_service_mock.assert_not_called()
