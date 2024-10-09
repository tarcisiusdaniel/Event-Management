from django.test import Client
from django.urls import reverse

import pytest
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from event.models import Event
from user.models import User
from .models import Registration
from user.views import jwt_handler
import json

@pytest.fixture
def client():
    """
    Set up client
    """
    return Client()

@pytest.fixture
def user():
    """
    Set up User object that will be used to call the Event's APIs
    """
    user = User.objects.create(
        email = "test123@gmail.com",
        first_name = "test",
        last_name = "123"
    )
    return user

@pytest.fixture
def event(user):
    """
    Set up the event created by a User
    """
    user_event = Event.objects.create(
        title = "The Title for Test123 Event",
        description = "This is the test description for Test123 event. Testing purposes",
        date = "2024-10-12",
        location = "9999 51st Ave W, TestCity, WA 98012",
        created_by = user,
    )
    return user_event

@pytest.fixture
def jwt_setup(user, client):
    """
    Setup JWT, and return the JWT token
    """
    jwt_response = jwt_handler(user.email, user.first_name, user.last_name, user.id)
    jwt_token = jwt_response['jwt_token']
    client.cookies['jwt_token'] = jwt_token
    return jwt_token

@pytest.mark.django_db
def test_register_user_to_event_success(client, user, jwt_setup, event):
    """
    Test registering the logged in user to an event successfully
    """
    url = reverse('Register User to an Event', kwargs = {'event_id': event.id})
    response = client.post(url)

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)
    
    assert response_json_data['status_code'] == 200
    assert response_json_data['status'] == "Success"
    assert Registration.objects.filter(user = user.id, event = event.id)

@pytest.mark.django_db
def test_register_user_to_event_user_not_exist(client, user, jwt_setup, event):
    """
    Test registering the logged in user to an event, but fail because the event does not exist
    """
    non_exist_user_jwt_response = jwt_handler("nonexist@gmail.com", "Non", "Exist", 809)
    non_exist_user_jwt_token = non_exist_user_jwt_response['jwt_token']
    client.cookies['jwt_token'] = non_exist_user_jwt_token

    url = reverse('Register User to an Event', kwargs = {'event_id': 2141})
    response = client.post(url)

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)
    
    assert response_json_data['status_code'] == 500
    assert response_json_data['description'] == "User does not exists in the database"

@pytest.mark.django_db
def test_register_user_to_event_fail(client, user, jwt_setup, event):
    """
    Test registering the logged in user to an event, but fail because the event does not exist
    """
    url = reverse('Register User to an Event', kwargs = {'event_id': 2141})
    response = client.post(url)

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)
    
    assert response_json_data['status_code'] == 404
    assert response_json_data['status'] == "Failed"
    assert response_json_data['description'] == "Event does not exist"
    assert not Registration.objects.filter(user = user.id, event = event.id)

@pytest.mark.django_db
def test_register_user_to_event_no_duplication(client, user, jwt_setup, event):
    """
    Test registering the logged in user to an event, but fail because the event does not exist
    """
    test_register_user_to_event_success(client, user, jwt_setup, event)
    url = reverse('Register User to an Event', kwargs = {'event_id': event.id})
    response = client.post(url)

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)
    
    assert response_json_data['status_code'] == 202
    assert response_json_data['status'] == "No action"
    assert response_json_data['description'] == "Registration not created. Already registered"
    assert len(Registration.objects.filter(user = user.id, event = event.id)) == 1