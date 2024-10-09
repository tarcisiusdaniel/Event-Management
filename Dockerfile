FROM python:3.12

# Set build arguments
# ARG GOOGLE_OAUTH_CLIENT_ID
# ARG GOOGLE_OAUTH_CLIENT_SECRET
# ARG DB_NAME
# ARG DB_USER
# ARG DB_PASSWORD
# ARG DB_HOST
# ARG JWT_SECRET

# Set environment variables using build arguments
# ENV GOOGLE_OAUTH_CLIENT_ID=$GOOGLE_OAUTH_CLIENT_ID
# ENV GOOGLE_OAUTH_CLIENT_SECRET=$GOOGLE_OAUTH_CLIENT_SECRET
# ENV DB_NAME=$DB_NAME
# ENV DB_USER=$DB_USER
# ENV DB_PASSWORD=$DB_PASSWORD
# ENV DB_HOST=$DB_HOST
# ENV JWT_SECRET=$JWT_SECRET

ENV PYTHONUNBUFFERED=1

WORKDIR /event_management_backend

# COPY . .env requirements.txt entrypoint.sh /event_management_backend/

COPY . requirements.txt entrypoint.sh /event_management_backend/

EXPOSE 8000

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]



