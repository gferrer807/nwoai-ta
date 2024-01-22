from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

mongo_uri = "mongodb://localhost:27017/"
client = MongoClient(mongo_uri)
db = client["test"]
collection = db["data_collection"]

def write_to_db(data):
    try:
        client.admin.command('ping')
    except ConnectionFailure:
        print("MongoDB connection failed")
        return
    
    try:
        result = collection.insert_one(data)
        print(f"Data inserted with record id {result.inserted_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the MongoDB connection
        client.close()
