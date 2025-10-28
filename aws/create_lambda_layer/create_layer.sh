#!/bin/bash

# Set the directory where the Dockerfile and requirements.txt are located
DIRECTORY="$(pwd)"

# Change it as per your requirement
LAYER_NAME="ops-chatbot-playwright-layer"
# Copy the requirements.txt file to the current directory
#cp ../../../requirements.txt requirements.txt

# Build the Docker image
docker build -f Dockerfile_playwright -t lambda-layers "$DIRECTORY"

# Run the Docker container to create the layers
docker run --name lambda-layers-container -v "$DIRECTORY:/app" lambda-layers

# create layers directory, if not created.
mkdir -p layers

# Move the zip file in layers directory.
mv "$DIRECTORY/$LAYER_NAME.zip" "$DIRECTORY/layers/$LAYER_NAME.zip"

# Stop the container
docker stop lambda-layers-container

# Remove the running container
docker rm lambda-layers-container

# Cleanup: remove the Docker image
docker rmi --force lambda-layers
