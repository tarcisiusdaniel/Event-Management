#!/bin/sh

echo "Starting Docker installation..."

# Install Docker
sudo yum update  -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
# sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

echo "Finished Docker installation..."