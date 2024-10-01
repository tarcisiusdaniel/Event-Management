# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from event.models import Event
from user.models import User
from user.views import user_auth_jwt
from .models import Registration
import json

# Create your views here.
def auth_user(request):
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

# •	Allow users to register for an event:
# •	A user can register for any event.
# •	A user cannot register for the same event twice.
# This allows the user to register to an event they created

def register_user_to_event(request, event_id):
    """
    The API that handles registering user to an event
    """
    auth_response = auth_user(request)
    if auth_response['status_code'] == 401:
        return JsonResponse(auth_response)
    # extract user info after authentication
    user_info = auth_response['user_info']

    if request.method == 'POST':
        # post the registration to the registration table
        # if the user is already registered for the event, then abort the operation
        try :
            event = Event.objects.get(id = event_id)
            user = User.objects.get(id = user_info['id'])
            tuple = Registration.objects.get(user = user_info['id'], event = event_id)
        except Event.DoesNotExist:
            return JsonResponse({
                'status_code': 404,
                'status': "Failed",
                'description': "Event does not exist"
            })
        except Registration.DoesNotExist:
            new_registration = Registration(user = user, event = event)
            new_registration.save()
            return JsonResponse({
                'status_code': 200,
                'status': "Success",
                'description': "Registration created"
            })
        
    return JsonResponse({
        'status_code': 202,
        'status': "No action",
        'description': "Registration not created. Already registered"
    })



