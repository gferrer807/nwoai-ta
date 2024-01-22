import json
import base64
import requests

GOLD_URL = 'http://gold:8080/insert'

def translate_schema(raw_data):
    data = raw_data['data']['data']

    media_previews = []
    if 'preview' in data and 'images' in data['preview']:
        for media in data['preview']['images']:
            media_previews.append({
                "url": media['source']['url'],
                "thumbnail": media['resolutions'][-1]['url']
            })
    try:
        id = data['id']
    except Exception as e:
        id = data['data']['id']
    return {
        "post_id": id,
        "title": data['title'],
        "created_utc_time": data['created_utc'],
        "score": data['score'],
        "num_comments": data['num_comments'],
        "subreddit": {
            "name": data['subreddit'],
            "subscribers": data['subreddit_subscribers']
        },
        "author": {
            "name": data['author'],
            "full_name": data['author_fullname'] if 'author_fullname' in data else None,
            "premium_status": data['author_premium'] if 'author_premium' in data else None,
        },
        "media": media_previews,
        "permalink": data['permalink'],
    }

def send_to_gold(data):
    # Construct the Pub/Sub message envelope and data payload
    pubsub_message = {
        "message": {
            "data": base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8"),
            "attributes": {},
            "messageId": "fake-message-id"
        },
        "subscription": "projects/fake-project/subscriptions/fake-subscription"
    }
    
    # URL of the Silver service, using HTTP and the correct port
    url = GOLD_URL

    try:
        # Sending the constructed message
        response = requests.post(url, json=pubsub_message)
        if response.status_code == 200:
            print("Message sent successfully to Gold service.")
        else:
            print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"An error occurred while sending message to Gold service: {e}")
