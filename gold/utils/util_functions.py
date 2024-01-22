from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def write_to_db(data):
    mongo_uri = "mongodb://localhost:27017/"
    client = MongoClient(mongo_uri)
    
    try:
        client.admin.command('ping')
    except ConnectionFailure:
        print("MongoDB connection failed")
        return
    
    db = client["test"]
    collection = db["data_collection"]
    
    try:
        result = collection.insert_one(data)
        print(f"Data inserted with record id {result.inserted_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the MongoDB connection
        client.close()
