#!/usr/bin/env bash

# Note: This relies on the dockerfile being updated with the latest version number (as there doesn't seem to be a latest tag for the HA RPI container). It will also leave behind the old HA RPI image. 

# Stop the existing container
docker stop homeassistant

# Delete the existing container
docker rm homeassistant

# Delete the existing image
docker rmi myhomeassistant:latest

# Change Directory
cd /home/pi/homeassistant/docker

# Run the docker compose file
docker-compose up -d
