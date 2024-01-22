from pymongo import MongoClient, UpdateOne
from bson.objectid import ObjectId
from datetime import datetime

# Setup MongoDB connection
client = MongoClient("mongodb://root:rootpassword@mongodb_container:27017/")
db = client['test']

# Example for insert_author_if_not_exists
def insert_author_if_not_exists(author_data):
    existing_author = db.authors.find_one({"name": author_data['author']})
    if existing_author:
        return str(existing_author['_id'])  # Convert ObjectId to string
    else:
        insert_result = db.authors.insert_one({
            "name": author_data['author'],
            "full_name": author_data.get('author_fullname'),
            "premium_status": author_data.get('author_premium', False)
        })
        return str(insert_result.inserted_id)  # Convert ObjectId to string


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

    media_previews = []
    if 'preview' in data and 'images' in data['preview']:
        for media in data['preview']['images']:
            media_previews.append({
                "url": media['source']['url'],
                # Use the last resolution available as the thumbnail
                "thumbnail": media['resolutions'][-1]['url'] if media['resolutions'] else None
            })

    # Upsert subreddit, author, and media documents and retrieve their Object IDs
    subreddit_id = upsert_subreddit(data['subreddit'], data['created'])
    author_id = insert_author_if_not_exists(data)

    # Extract post ID with fallback
    post_id = data.get('id', data.get('data', {}).get('id'))

    return {
        "post_id": post_id,
        "title": data['title'],
        "created_utc_time": data['created_utc'],
        "score": data['score'],
        "num_comments": data['num_comments'],
        "subreddit_id": subreddit_id,  # Attach the subreddit ID
        "author_id": author_id,  # Attach the author ID
        "media_ids": None,  # Attach the list of media IDs
        "permalink": data['permalink'],
    }