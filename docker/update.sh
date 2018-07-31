#!/usr/bin/env bash

# Note: This script will leave behind old HA RPI images. 

# Ask for target version
read -p "What version of Home Assistant would you like to install? " version
printf "\n"

# Pull the image
docker pull homeassistant/raspberrypi3-homeassistant:$version || exit 1

# Create a new docker-compose file from the docker-compose-template file using the target version number
version_token="{{ version }}"

sed -e "s/${version_token}/${version}/g" \
    < docker-compose-template.yaml \
    > docker-compose.yaml || exit 1

printf "Disabling Hass Watcher..."
wget -qO- https://reactor.dullage.com/timedjob/Hass%20Watcher/disable
printf "\n"
	
# Stop the existing container
docker stop homeassistant

# Delete the existing container
docker rm homeassistant

# Run the docker compose file
docker-compose up -d

printf "Waiting for 80 seconds for Homassistant to Boot...\n"
sleep 80

printf "Re-Enabling Hass Watcher..."
wget -qO- https://reactor.dullage.com/timedjob/Hass%20Watcher/enable
printf "\n"
