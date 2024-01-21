from google.cloud import pubsub_v1
import os

# Ensure the emulator's host is correctly set
pubsub_emulator_host = os.getenv("PUBSUB_EMULATOR_HOST")
print(f"Using PUBSUB_EMULATOR_HOST: {pubsub_emulator_host}")

project_id = "fake-project"
subscription_id = "my-subscription"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    print(f"Received message: {message.data.decode('utf-8')}")
    # Process the message here
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...")

def main():
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()