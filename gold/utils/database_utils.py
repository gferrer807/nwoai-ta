import os
from pymongo import MongoClient
from bson.objectid import ObjectId

MONGO_USER = os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'root')
MONGO_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD', 'rootpassword')
MONGO_HOST = os.environ.get('MONGO_HOST', 'mongodb_container')
MONGO_DB = os.environ.get('MONGO_DB')

mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:27017/"
client = MongoClient(mongo_uri)
db = client[MONGO_DB]

def prepare_and_insert_posts(decoded_data):
    """
    Prepares post data by converting string IDs to ObjectIds and inserts the data into the MongoDB collection.

    :param decoded_data: The JSON-decoded data received from the request.
    :return: A tuple of (success, message) where success is a boolean indicating the operation's outcome.
    """
    for element in decoded_data:
        # Convert string IDs to ObjectIds
        element['subreddit_id'] = ObjectId(element['subreddit_id'])
        element['author_id'] = ObjectId(element['author_id'])
        element['media_ids'] = [ObjectId(id_str) for id_str in element.get('media_ids', [])]

    try:
        # Insert the prepared data into the 'posts' collection
        result = db['posts'].insert_many(decoded_data)
        # Successfully inserted
        return True, f"Data inserted successfully, inserted_ids: {[str(id_) for id_ in result.inserted_ids]}"
    except Exception as e:
        # An error occurred
        return False, str(e)
