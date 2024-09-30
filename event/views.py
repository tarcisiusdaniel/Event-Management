from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from user.views import user_auth_jwt
import jwt, datetime, json
from .models import Event
from user.models import User

import os
from dotenv import load_dotenv


load_dotenv()

# Create your views here.

# In here, always check the authorization of the API caller 

def index(request):
    """
    The index view for event model
    """
    auth_response = json.loads(user_auth_jwt(request).content)
    auth_response_status = auth_response.get("status")

    if auth_response_status == 'Failed':
        return HttpResponse(auth_response.get("description"))

    return HttpResponse("Hello World")

# •	Create: Users should be able to create events.
def create_event(request):
    """
    API to Create an event for the user
    """
    auth_response = json.loads(user_auth_jwt(request).content)
    auth_response_status = auth_response.get("status")

    if auth_response_status == 'Failed':
        return HttpResponse(auth_response.get("description"))
    
    # extract user info after authentication
    user_info = auth_response.get("user_info")
    
    # create the event using POST request
    if request.method == 'POST':
        decoded_string = request.body.decode('utf-8')
        json_data = json.loads(decoded_string)

        new_event = Event(
            title = json_data['title'],
            description = json_data['description'],
            date = json_data['date'],
            location = json_data['location'],
            created_by = User.objects.get(
                email = user_info['email'], 
                first_name = user_info['first_name'], 
                last_name = user_info['last_name']
            ),
        )
        new_event.save()
    
    return HttpResponse("Done")

# •	Retrieve: Users should be able to view a list of events of certain user.
def retrieve_events_by_user_id(request, user_id):
    """
    API to get events created by the user
    """
    auth_response = json.loads(user_auth_jwt(request).content)
    auth_response_status = auth_response.get("status")

    if auth_response_status == 'Failed':
        return HttpResponse(auth_response.get("description"))

    user_events = []
    # retrieve the events using GET request
    if request.method == 'GET':
        # check if the id is valid
        try:
            user_info = User.objects.get(id = user_id)
            user_events_objects = Event.objects.filter(
                created_by = user_info.id
            )
            user_events = [{
                "title": event.title,
                "description": event.description,
                'date': event.date,
                'location': event.description,
                'created_by': {
                    'email': event.created_by.email,
                    'first_name': event.created_by.first_name,
                    'last_name': event.created_by.last_name,
                },
            } for event in user_events_objects]
            # print(user_events)
        except User.DoesNotExist:
            return JsonResponse({
                'status': "Failed",
                'description': "The user does not exist"
            })

    return JsonResponse({
        'user_events': user_events
    })

# •	Retrieve: Users should be able to view a list of his/her events
def retrieve_events(request):
    """
    API to get events created by the user
    """
    auth_response = json.loads(user_auth_jwt(request).content)
    auth_response_status = auth_response.get("status")

    if auth_response_status == 'Failed':
        return HttpResponse(auth_response.get("description"))
    
    # extract user info after authentication
    user_info = auth_response.get("user_info")

    user_events = []

    # retrieve the events using GET request
    if request.method == 'GET':
        # try:
        user_events_objects = Event.objects.filter(
            created_by = user_info['id']
        )
        user_events = [{
            "title": event.title,
            "description": event.description,
            'date': event.date,
            'location': event.description,
            'created_by': {
                'email': event.created_by.email,
                'first_name': event.created_by.first_name,
                'last_name': event.created_by.last_name,
            },
        } for event in user_events_objects]
        # print(user_events)

    return JsonResponse({
        'user_events': user_events
    })

# •	Update: Users can update the events they created.
# update can be not done because the event is not user's
# the event does not exist
def update_event(request, event_id):
    """
    API to Update an event for the user
    """
    auth_response = json.loads(user_auth_jwt(request).content)
    auth_response_status = auth_response.get("status")

    if auth_response_status == 'Failed':
        return HttpResponse(auth_response.get("description"))
    
    # extract user info after authentication
    user_info = auth_response.get("user_info")

    # update an event using PUT request
    if request.method == 'PUT':
        decoded_string = request.body.decode('utf-8')
        json_data = json.loads(decoded_string)

        event_to_update = Event.objects.filter(
            id = event_id,
            created_by = user_info['id']
        )
        
        updated_count = event_to_update.update(
            title = json_data['title'],
            description = json_data['description'],
            date = json_data['date'],
            location = json_data['location']
        )

        if (updated_count > 0):
            return HttpResponse("Updated count: " + f'{updated_count}')

    return HttpResponse("No update done")

# •	Delete: Users can delete the events they created.
# delete can be not done because the event is not user's
# the event does not exist
def delete_event(request, event_id):
    """
    API to Create an event for the user
    """
    auth_response = json.loads(user_auth_jwt(request).content)
    auth_response_status = auth_response.get("status")

    if auth_response_status == 'Failed':
        return HttpResponse(auth_response.get("description"))
    
    # extract user info after authentication
    user_info = auth_response.get("user_info")

    # delete an event using DELETE request
    if request.method == 'DELETE':
        event_to_delete = Event.objects.filter(
            id = event_id,
            created_by = user_info['id']
        )
        deleted_count, _ = event_to_delete.delete()
        if (deleted_count > 0):
            return HttpResponse("Delete count: " + f'{deleted_count}')

    return HttpResponse("No deletion")