from pymongo import MongoClient, UpdateOne
from bson.objectid import ObjectId
from datetime import datetime
import os

MONGO_DB = os.environ.get('MONGO_DB')
MONGO_USER = os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'root')
MONGO_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD', 'rootpassword')
MONGO_HOST = os.environ.get('MONGO_HOST', 'mongodb_container')

mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:27017/"

client = MongoClient(mongo_uri)
db = client[MONGO_DB]

def insert_media_if_not_exists(media_data, post_id):
    """
    Inserts a new media document if it does not already exist.
    
    :param media_data: A dictionary containing the media's details.
    :param post_id: The ID of the post associated with this media.
    :return: The ObjectId of the media document.
    """
    existing_media = db.media.find_one({"url": media_data['url']})

    if existing_media:
        # If the media exists but the current post_id is not associated, update the document
        if post_id not in existing_media.get('post_ids', []):
            db.media.update_one(
                {"_id": existing_media['_id']},
                {"$push": {"post_ids": post_id}}
            )
        return str(existing_media['_id'])
    else:
        # Insert the new media document
        insert_result = db.media.insert_one({
            "url": media_data['url'],
            "post_ids": [post_id],  # Initialize with the current post_id
            "media_content": media_data.get('resolutions', [])  # Optional: include resolution details
        })
        return str(insert_result.inserted_id)

def insert_author_if_not_exists(author_data):
    existing_author = db.authors.find_one({"name": author_data['author']})
    if existing_author:
        return str(existing_author['_id'])
    else:
        insert_result = db.authors.insert_one({
            "name": author_data['author'],
            "full_name": author_data.get('author_fullname'),
            "premium_status": author_data.get('author_premium', False)
        })
        return str(insert_result.inserted_id)


def upsert_subreddit(subreddit_name, update_date_utc):
    update_date = datetime.utcfromtimestamp(update_date_utc)

    existing_doc = db.subreddits.find_one({"name": subreddit_name}, {"last_updated_date": 1})

    if existing_doc and "last_updated_date" in existing_doc:
        if existing_doc["last_updated_date"] < update_date:
            result = db.subreddits.update_one(
                {"_id": existing_doc["_id"]},
                {
                    "$set": {"last_updated_date": update_date},
                    "$setOnInsert": {"name": subreddit_name}
                },
                upsert=True
            )
            return str(existing_doc["_id"])
        else:
            return str(existing_doc["_id"])
    else:
        result = db.subreddits.update_one(
            {"name": subreddit_name},
            {
                "$setOnInsert": {"name": subreddit_name, "last_updated_date": update_date},
            },
            upsert=True
        )
        if result.upserted_id:
            return str(result.upserted_id)
        else:
            return str(db.subreddits.find_one({"name": subreddit_name}, {"_id": 1})["_id"])
    
def process_data(raw_data):
    data = raw_data['data']['data']

    # Upsert subreddit and author documents and retrieve their Object IDs
    subreddit_id = upsert_subreddit(data['subreddit'], data['created'])
    author_id = insert_author_if_not_exists({
        'author': data['author'],
        'author_fullname': data.get('author_fullname'),
        'author_premium': data.get('author_premium', False)
    })

    # Extract post ID with fallback
    post_id = data.get('id', data.get('data', {}).get('id'))

    media_ids = []
    if 'preview' in data and 'images' in data['preview']:
        for media in data['preview']['images']:
            # Process each media item and insert if not exists, then collect the media ID
            media_id = insert_media_if_not_exists({
                "url": media['source']['url'],
                "resolutions": media.get('resolutions', [])  # Include resolution details if needed
            }, post_id)
            media_ids.append(media_id)

    return {
        "post_id": post_id,
        "title": data['title'],
        "created_utc_time": data['created_utc'],
        "score": data['score'],
        "num_comments": data['num_comments'],
        "subreddit_id": subreddit_id,
        "author_id": author_id,
        "media_ids": media_ids,
        "permalink": data['permalink'],
    }