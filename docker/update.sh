#!/usr/bin/env bash

# Note: This relieis on the dockerfile being updated with the latest version number (as there doesn't seem to be a latest tage for the HA RPI container). It will also leave behind the old HA RPI image.

# Change Directory
cd /home/pi/homeassistant/docker

# Stop the existing container
docker stop homeassistant

# Delete the existing container
docker rm homeassistant

# Delete the existing image
docker rmi myhomeassistant:latest

# Run the docker compose file
docker-compose up -d