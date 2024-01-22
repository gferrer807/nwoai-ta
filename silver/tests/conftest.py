import pytest
from app import app as flask_app
from unittest.mock import MagicMock
from pymongo.collection import Collection
import base64
import json
from .test_constants import TEST_PAYLOAD, TEST_PAYLOAD_RAW

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mongo_mock(mocker):
    # Mock the MongoClient
    mocker.patch('utils.database_utils.MongoClient', MagicMock())
    # Create a mock database and collections
    mock_db = MagicMock()
    mocker.patch('utils.database_utils.db', mock_db)
    mock_subreddits_collection = mock_db.subreddits
    mock_authors_collection = mock_db.authors
    mock_media_collection = mock_db.media
    # Set the collections to behave like pymongo Collection instances
    mock_subreddits_collection.__class__ = Collection
    mock_authors_collection.__class__ = Collection
    mock_media_collection.__class__ = Collection
    return mock_db

@pytest.fixture
def pubsub_message_data():
    return {
        'message': {
            'data': base64.b64encode(json.dumps(TEST_PAYLOAD_RAW).encode('utf-8')).decode('utf-8'),
            'attributes': {},
            'messageId': 'test-message-id'
        },
        'subscription': 'test-subscription'
    }

@pytest.fixture
def gold_service_mock(mocker):
    return mocker.patch('app.send_to_gold', return_value=None)