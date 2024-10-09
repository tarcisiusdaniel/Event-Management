#!/bin/sh

# # Start Docker service
# sudo service docker start

# # Navigate to the directory with the docker-compose.yml
# cd /home/ec2-user/event_management

# # Set the AWS region
# export AWS_REGION="us-east-1"  # Adjust as necessary

# # Fetch parameters from Parameter Store and export them as environment variables
# export GOOGLE_OAUTH_CLIENT_ID=$(aws ssm get-parameter --name "/event_management_backend/GOOGLE_OAUTH_CLIENT_ID" --query "Parameter.Value" --output text --region us-east-1)
# export GOOGLE_OAUTH_CLIENT_SECRET=$(aws ssm get-parameter --name "/event_management_backend/GOOGLE_OAUTH_CLIENT_SECRET" --query "Parameter.Value" --output text --region us-east-1)
# export DB_NAME=$(aws ssm get-parameter --name "/event_management_backend/DB_NAME" --query "Parameter.Value" --output text --region us-east-1)
# export DB_USER=$(aws ssm get-parameter --name "/event_management_backend/DB_USER" --query "Parameter.Value" --output text --region us-east-1)
# export DB_PASSWORD=$(aws ssm get-parameter --name "/event_management_backend/DB_PASSWORD" --query "Parameter.Value" --output text --region us-east-1)
# export DB_HOST=$(aws ssm get-parameter --name "/event_management_backend/DB_HOST" --query "Parameter.Value" --output text --region us-east-1)
# export JWT_TOKEN=$(aws ssm get-parameter --name "/event_management_backend/JWT_SECRET" --query "Parameter.Value" --output text --region us-east-1)

# # Start Docker containers
# docker-compose up --build -d