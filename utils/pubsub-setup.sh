#!/bin/bash

HOST="pubsub-emulator"
PORT=8085
TOPIC="my-topic"

# http://pubsub-emulator:8085/v1/projects/fake-project/topics/

wait_for_emulator() {
    echo "Waiting for Pub/Sub emulator to start..."
    until curl -s http://${HOST}:${PORT}; do   
        echo "Waiting for Pub/Sub emulator to be available at ${HOST}:${PORT}..."
        sleep 1
    done
    echo "Pub/Sub emulator is up and running!"
}

create_topic() {
    echo "Creating topic '${TOPIC}'..."
    curl -X PUT http://${HOST}:${PORT}/v1/projects/fake-project/topics/${TOPIC}
    echo "Topic '${TOPIC}' created."
}

create_subscription() {
    echo "Creating subscription 'my-subscription'..."
    curl -X PUT http://${HOST}:${PORT}/v1/projects/fake-project/subscriptions/my-subscription \
        -H "Content-Type: application/json" \
        -d "{\"topic\": \"projects/fake-project/topics/${TOPIC}\"}"
    echo "Subscription 'my-subscription' created."
}

wait_for_emulator

create_topic

create_subscription