import pytest
from app import app as flask_app

TEST_MONGO_DB = 'test_db'

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mongo_mock(mocker):
    mongo_client_mock = mocker.patch('utils.database_utils.MongoClient')
    mock_db = mongo_client_mock.return_value[TEST_MONGO_DB]
    mock_collection = mock_db['posts']
    return mock_collection
