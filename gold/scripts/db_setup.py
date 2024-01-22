from pymongo import MongoClient

mongo_user = 'root'
mongo_pass = 'rootpassword'
mongo_host = 'mongodb_container'
mongo_port = '27017'
database_name = 'reddit_analytics'
collections = ['posts', 'authors', 'media', 'subreddits']

client = MongoClient(f'mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/')

db = client[database_name]

for collection in collections:
    db.create_collection(collection)

print(f"Database '{database_name}' and collections {collections} have been created successfully.")