#!/bin/bash

# Build the Docker image
sudo docker build -t usamaasaleeem/max:latest .
if [ $? -ne 0 ]; then
    echo "Docker build failed."
    exit 1
fi

# Push the Docker image to the repository
# sudo docker push usamaasaleeem/max:latest
# if [ $? -ne 0 ]; then
#     echo "Docker push failed."
#     exit 1
# fi

echo "Docker build and push completed successfully."