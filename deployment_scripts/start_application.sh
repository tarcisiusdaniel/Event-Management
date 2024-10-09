#!/bin/sh

# # Start Docker service
# sudo service docker start

# Navigate to the directory with the docker-compose.yml
cd /home/ec2-user/event_management

Start Docker containers
docker-compose up --build -d