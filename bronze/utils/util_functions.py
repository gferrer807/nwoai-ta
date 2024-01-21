def process_jsonl_file(filepath, publisher, topic_name):
    print(f'Processing file: {filepath}')
    with open(filepath, 'r') as file:
        for line in file:
            print(f'Processing line: {line}')
            data = line.encode('utf-8')
            try:
                publish_future = publisher.publish(topic_name, data)
                publish_future.result()  # Verify the publish succeeded
            except Exception as e:
                print(f'An error occurred: {e}')
    try:
        publish_message('hello world')
    except Exception as e:
        Exception(f'An error occurred reading file and publishing to pubsub: {e}')

def publish_message(data, publisher, topic_path):
    # Data must be a bytestring
    try:
        data = data.encode("utf-8")
        future = publisher.publish(topic_path, data)
        print(f"Published {data} to {topic_path}.", flush=True)
    except Exception as e:
        print(f'An error occurred: {e}', flush=True)