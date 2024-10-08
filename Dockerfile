FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /event_management_backend

# COPY . .env requirements.txt entrypoint.sh /event_management_backend/

COPY . requirements.txt entrypoint.sh /event_management_backend/

EXPOSE 8000

# run when deployed to aws ec2
RUN yum install -y aws-cli

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]



