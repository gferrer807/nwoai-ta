from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def write_to_db(data):
    mongo_uri = "mongodb://root:rootpassword@mongodb_container:27017/"
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    db = client["test"]
    collection = db["data_collection"]

    print('Attempting to write in db...', flush=True)
    try:
        for element in data:
            print("Attempting to insert data:", element, flush=True)
            result = collection.insert_one(element)
            print(f"Data inserted with record id {result.inserted_id}", flush=True)
    except Exception as e:
        print(f"An error occurred during insertion: {e}", flush=True)
    finally:
        client.close()
