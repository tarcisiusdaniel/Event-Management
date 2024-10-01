# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from user.views import user_auth_jwt
import jwt, datetime, json
from .models import Event
from user.models import User


def auth_user(request):
    """
    Authenticate the current user
    """
    auth_response = json.loads(user_auth_jwt(request).content)
    auth_response_status = auth_response.get("status")
    
    if auth_response_status == 'Failed':
        return {
            'status_code': 401,
            'description': auth_response.get("description"),
            'user_info': {}
        }
    
    # extract user info after authentication
    user_info = auth_response.get("user_info")

    return {
        'status_code': 200,
        'description': "Authorized",
        'user_info': user_info
    }

# •	Create: Users should be able to create events.
def create_event(request):
    """
    API to Create an event for the user
    """
    auth_response = auth_user(request)
    if auth_response['status_code'] == 401:
        return JsonResponse(auth_response)
    # extract user info after authentication
    user_info = auth_response['user_info']
    
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
    
    return JsonResponse({
        'status_code': 201,
        'status': "Success",
        'description': "Successfully create event"
    })

# •	Retrieve: Users should be able to view a list of events of certain user.
def retrieve_events_by_user_id(request, user_id):
    """
    API to get events created by the user
    """
    auth_response = auth_user(request)
    if auth_response['status_code'] == 401:
        return JsonResponse(auth_response)
    # # extract user info after authentication
    # user_info = auth_response['user_info']

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
                'location': event.location,
                'created_by': {
                    'email': event.created_by.email,
                    'first_name': event.created_by.first_name,
                    'last_name': event.created_by.last_name,
                },
            } for event in user_events_objects]
            # print(user_events)
        except User.DoesNotExist:
            return JsonResponse({
                'status_code': 404,
                'status': "Failed",
                'description': "The user does not exist"
            })

    return JsonResponse({
        'status_code': 200,
        'status': "Success",
        'user_events': user_events
    })

# •	Retrieve: Users should be able to view a list of his/her events
def retrieve_events(request):
    """
    API to get events created by the user
    """
    auth_response = auth_user(request)
    if auth_response['status_code'] == 401:
        return JsonResponse(auth_response)
    # extract user info after authentication
    user_info = auth_response['user_info']

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
            'location': event.location,
            'created_by': {
                'email': event.created_by.email,
                'first_name': event.created_by.first_name,
                'last_name': event.created_by.last_name,
            },
        } for event in user_events_objects]
        # print(user_events)

    return JsonResponse({
        'status_code': 200,
        'status': "Success",
        'user_events': user_events
    })

# •	Update: Users can update the events they created.
# update can be not done because the event is not user's
# the event does not exist
def update_event(request, event_id):
    """
    API to Update an event for the user
    """
    auth_response = auth_user(request)
    if auth_response['status_code'] == 401:
        return JsonResponse(auth_response)
    # extract user info after authentication
    user_info = auth_response['user_info']

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
            return JsonResponse({
                'status_code': 200,
                'status': "Success",
                'updated_count': updated_count
            })

    return JsonResponse({
        'status_code': 404,
        'status': "Failed",
        'updated_count': 0
    })

# •	Delete: Users can delete the events they created.
# delete can be not done because the event is not user's
# the event does not exist
def delete_event(request, event_id):
    """
    API to Create an event for the user
    """
    auth_response = auth_user(request)
    if auth_response['status_code'] == 401:
        return JsonResponse(auth_response)
    # extract user info after authentication
    user_info = auth_response['user_info']

    # delete an event using DELETE request
    if request.method == 'DELETE':
        event_to_delete = Event.objects.filter(
            id = event_id,
            created_by = user_info['id']
        )
        deleted_count, tuple = event_to_delete.delete()
        if (deleted_count > 0):
            return JsonResponse({
                'status_code': 200,
                'status': "Success",
                'deleted_count': deleted_count
            })

    return JsonResponse({
        'status_code': 404,
        'status': "Failed",
        'deleted_count': 0
    })
