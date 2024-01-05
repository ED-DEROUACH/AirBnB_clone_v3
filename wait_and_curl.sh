#!/bin/bash

SERVER_URL="http://0.0.0.0:5000/api/v1/states/"
MAX_RETRIES=30  # Adjust the number of retries as needed
RETRY_INTERVAL=5  # Adjust the interval between retries as needed

retries=0

while [ $retries -lt $MAX_RETRIES ]; do
    if curl -X GET $SERVER_URL; then
        echo "Server is ready, making request..."
        break
    else
        echo "Connection refused. Retrying in $RETRY_INTERVAL seconds..."
        sleep $RETRY_INTERVAL
        retries=$((retries + 1))
    fi
done

if [ $retries -eq $MAX_RETRIES ]; then
    echo "Timeout reached. Unable to connect to the server."
fi

