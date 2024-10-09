#!/bin/sh

# Start Docker service
sudo service docker start

# Navigate to the directory with the docker-compose.yml
cd /home/ec2-user/event_management

# Set the AWS region
export AWS_REGION="us-east-1"  # Adjust as necessary

# Fetch parameters from Parameter Store and export them as environment variables
export GOOGLE_OAUTH_CLIENT_ID=$(aws ssm get-parameter --name "/event_management_backend/GOOGLE_OAUTH_CLIENT_ID" --query "Parameters[0].Value" --output text)
export GOOGLE_OAUTH_CLIENT_SECRET=$(aws ssm get-parameter --name "/event_management_backend/GOOGLE_OAUTH_CLIENT_SECRET" --query "Parameters[0].Value" --output text)
export DB_NAME=$(aws ssm get-parameter --name "/event_management_backend/DB_NAME" --query "Parameters[0].Value" --output text)
export DB_USER=$(aws ssm get-parameter --name "/event_management_backend/DB_USER" --query "Parameters[0].Value" --output text)
export DB_PASSWORD=$(aws ssm get-parameter --name "/event_management_backend/DB_PASSWORD" --query "Parameters[0].Value" --output text)
export DB_HOST=$(aws ssm get-parameter --name "/event_management_backend/DB_HOST" --query "Parameters[0].Value" --output text)
export JWT_TOKEN=$(aws ssm get-parameter --name "/event_management_backend/JWT_SECRET" --query "Parameters[0].Value" --output text)

# Start Docker containers
docker-compose up --build