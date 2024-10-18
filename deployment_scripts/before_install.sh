#!/bin/sh

# # Update the system
# yum update -y

# # Install Docker
# yum install -y docker

# # Start the Docker service
# service docker start

# # Clean up old containers
# docker stop my_container || true
# docker rm my_container || true

# # Ensure there's enough disk space
# df -h

# Update package information
sudo yum update -y

# Install Docker (for Amazon Linux 2)
sudo amazon-linux-extras install docker

# Start Docker service
sudo service docker start

# Add ec2-user to Docker group
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
