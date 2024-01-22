from pymongo import MongoClient
from pymongo.errors import BulkWriteError

def write_to_db(data):
    mongo_uri = "mongodb://root:rootpassword@mongodb_container:27017/"
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    db = client["reddit_analytics"]
    collection = db["accidental_renaissance"]

    try:
        # replace insert_many bulk_write with list of operations if there are concerns of updating existing documents
        result = collection.insert_many(data)
    except BulkWriteError as bwe:
        print(f"Bulk write error occurred: {bwe.details}", flush=True)
    except Exception as e:
        print(f"An error occurred during insertion: {e}", flush=True)
    finally:
        client.close()