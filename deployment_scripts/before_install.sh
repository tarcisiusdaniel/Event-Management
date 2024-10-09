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

# Set the AWS region
export AWS_REGION="us-east-1"  # Adjust as necessary

# Fetch parameters from Parameter Store and export them as environment variables
export GOOGLE_OAUTH_CLIENT_ID=$(aws ssm get-parameter --name "GOOGLE_OAUTH_CLIENT_ID" --with-decryption --query "Parameter.Value" --output text)
export GOOGLE_OAUTH_CLIENT_SECRET=$(aws ssm get-parameter --name "GOOGLE_OAUTH_CLIENT_SECRET" --with-decryption --query "Parameter.Value" --output text)
export DB_NAME=$(aws ssm get-parameter --name "DB_NAME" --with-decryption --query "Parameter.Value" --output text)
export DB_USER=$(aws ssm get-parameter --name "DB_USER" --with-decryption --query "Parameter.Value" --output text)
export DB_PASSWORD=$(aws ssm get-parameter --name "DB_PASSWORD" --with-decryption --query "Parameter.Value" --output text)
export DB_HOST=$(aws ssm get-parameter --name "DB_HOST" --with-decryption --query "Parameter.Value" --output text)
export JWT_TOKEN=$(aws ssm get-parameter --name "JWT_SECRET" --with-decryption --query "Parameter.Value" --output text)

# Ensure Docker is running
# sudo service docker start