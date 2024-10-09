from django.test import Client
from django.urls import reverse

import pytest
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from .models import Event
from user.models import User
from user.views import jwt_handler
import json

# Create your tests here.
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
def event_id():
    """
    Set up the event ID created by a User
    """
    return [None]

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
def test_create_event(client, user, jwt_setup, event_id):
    """
    Test creating events    
    """
    data = {
        "title": "Test123 Event Title",
        "description": "Test123 Event description for testing",
        'date': '2024-01-01',
        'location': "12354 51st Test Ave N, TestCity WA 98413",
        'created_by': user.id
    }

    json_data = json.dumps(data)

    response = client.post(reverse('Create Event'), data = json_data, content_type = 'application/json')

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)

    assert response_json_data['status_code'] == 201
    assert response_json_data['status'] == "Success"
    # print(Event.objects.filter(title="Test123 Event Title")[0].id)
    assert Event.objects.filter(title="Test123 Event Title").exists()
    assert len(Event.objects.filter(title="Test123 Event Title")) == 1
    event_id[0] = Event.objects.filter(title="Test123 Event Title")[0].id
    # return Event.objects.filter(title="Test123 Event Title")[0].id
    # assert Event.objects.filter(title="Test123 Event Title")[0].id == 1

@pytest.mark.django_db
def test_create_event_user_not_exists(client, user, jwt_setup):
    """
    Test creating events, but fail because the logged in user does not exists 
    """
    data = {
        "title": "Test123 Event Title",
        "description": "Test123 Event description for testing",
        'date': '2024-01-01',
        'location': "12354 51st Test Ave N, TestCity WA 98413",
        'created_by': user.id
    }

    json_data = json.dumps(data)

    non_exist_user_jwt_response = jwt_handler("nonexist@gmail.com", "Non", "Exist", 809)
    non_exist_user_jwt_token = non_exist_user_jwt_response['jwt_token']
    client.cookies['jwt_token'] = non_exist_user_jwt_token
    
    response = client.post(reverse('Create Event'), data = json_data, content_type = 'application/json')

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)
    # print(response_json_data)

    assert response_json_data['status_code'] == 500
    assert response_json_data['description'] == "User does not exists in the database"

@pytest.mark.django_db
def test_retrieve_events_by_user_id_success(client, user, jwt_setup, event_id):
    """
    Test to get events of a user with certain user id successfully
    """
    test_create_event(client, user, jwt_setup, event_id)
    url = reverse("Retrieve Others Events", kwargs = {'user_id': user.id})
    response = client.get(url)

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)

    assert response_json_data['status_code'] == 200
    assert response_json_data['status'] == "Success"
    assert len(response_json_data['user_events']) > 0

@pytest.mark.django_db
def test_retrieve_events_by_user_id_fail(client, user, jwt_setup, event_id):
    """
    Test to get events of a user with certain user id but fail because user_id does not exist
    """
    test_create_event(client, user, jwt_setup, event_id)
    url = reverse('Retrieve Others Events', kwargs = {'user_id': 7821368})
    response = client.get(url)

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)

    assert response_json_data['status_code'] == 404
    assert response_json_data['status'] == "Failed"
    assert not hasattr(response_json_data, 'user_events')

# no need @pytest.mark.django_db
# because it goes to error right away after knowing the user is not authenticated
# no connecting to database
def test_retrieve_events_by_user_id_user_not_exist(client, user, jwt_setup, event_id):
    """
    Test to get events of a user with certain user id, but fail because the logged in user does not exist
    """
    test_create_event(client, user, jwt_setup, event_id)
    
    non_exist_user_jwt_response = jwt_handler("nonexist@gmail.com", "Non", "Exist", 809)
    non_exist_user_jwt_token = non_exist_user_jwt_response['jwt_token']
    client.cookies['jwt_token'] = non_exist_user_jwt_token

    url = reverse('Retrieve Others Events', kwargs = {'user_id': user.id})
    response = client.get(url)

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)

    assert response_json_data['status_code'] == 500
    assert response_json_data['description'] == "User does not exists in the database"

@pytest.mark.django_db
def test_retrieve_events(client, user, jwt_setup, event_id):
    """
    Test to get events of the current logged in user
    """
    test_create_event(client, user, jwt_setup, event_id)
    url = reverse('Retrieve Own Events')
    response = client.get(url)

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)

    assert response_json_data['status_code'] == 200
    assert response_json_data['status'] == "Success"
    assert len(response_json_data['user_events']) > 0

@pytest.mark.django_db
def test_retrieve_events_user_not_exist(client, user, jwt_setup, event_id):
    """
    Test to get events of the current logged in user, but the logged in user does not exist
    """
    test_create_event(client, user, jwt_setup, event_id)
    
    non_exist_user_jwt_response = jwt_handler("nonexist@gmail.com", "Non", "Exist", 809)
    non_exist_user_jwt_token = non_exist_user_jwt_response['jwt_token']
    client.cookies['jwt_token'] = non_exist_user_jwt_token

    url = reverse('Retrieve Own Events')
    response = client.get(url)

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)

    assert response_json_data['status_code'] == 500
    assert response_json_data['description'] == "User does not exists in the database"

@pytest.mark.django_db
def test_update_event_success(client, user, jwt_setup, event_id):
    """
    Test to update an event of the current logged in user successfully
    """
    test_create_event(client, user, jwt_setup, event_id)

    new_data = {
        "title": "Test123 Event New Title From Update",
        "description": "Test123 Event description for testing. This is the neew updated description",
        'date': '2024-02-02',
        'location': "51423 99st Test Ave W, TestCity WA 98413",
    }

    json_data = json.dumps(new_data)
    url = reverse('Update Event', kwargs = {'event_id': event_id[0] })
    response = client.put(url, data = json_data, content_type = 'application/json')

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)

    assert response_json_data['status_code'] == 200
    assert response_json_data['status'] == "Success"
    assert response_json_data['updated_count'] == 1
    assert Event.objects.filter(title="Test123 Event New Title From Update").exists()

@pytest.mark.django_db
def test_update_event_user_not_exist(client, user, jwt_setup, event_id):
    """
    Test to update an event of the current logged in user, but fail because the logged in user does not exists
    """
    test_create_event(client, user, jwt_setup, event_id)

    new_data = {
        "title": "Test123 Event New Title From Update",
        "description": "Test123 Event description for testing. This is the neew updated description",
        'date': '2024-02-02',
        'location': "51423 99st Test Ave W, TestCity WA 98413",
    }

    json_data = json.dumps(new_data)

    non_exist_user_jwt_response = jwt_handler("nonexist@gmail.com", "Non", "Exist", 809)
    non_exist_user_jwt_token = non_exist_user_jwt_response['jwt_token']
    client.cookies['jwt_token'] = non_exist_user_jwt_token

    url = reverse('Update Event', kwargs = {'event_id': event_id[0] })
    response = client.put(url, data = json_data, content_type = 'application/json')

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)

    assert response_json_data['status_code'] == 500
    assert response_json_data['description'] == "User does not exists in the database"

@pytest.mark.django_db
def test_update_event_fail(client, user, jwt_setup, event_id):
    """
    Test to update an event of the current logged in user but fail because the id wanted to be updated does not exist
    """
    test_create_event(client, user, jwt_setup, event_id)

    new_data = {
        "title": "Test123 Event New Title From Update",
        "description": "Test123 Event description for testing. This is the neew updated description",
        'date': '2024-02-02',
        'location': "51423 99st Test Ave W, TestCity WA 98413",
    }

    json_data = json.dumps(new_data)

    url = reverse('Update Event', kwargs = {'event_id': 300 })
    response = client.put(url, data = json_data, content_type = 'application/json')

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)

    assert response_json_data['status_code'] == 404
    assert response_json_data['status'] == "Failed"
    assert response_json_data['updated_count'] == 0
    assert not Event.objects.filter(title="Test123 Event New Title From Update").exists()

@pytest.mark.django_db
def test_delete_event_success(client, user, jwt_setup, event_id):
    """
    Test to delete an event of the current logged in user successfully
    """
    test_create_event(client, user, jwt_setup, event_id)

    url = reverse('Delete Event', kwargs = {'event_id': event_id[0] })
    response = client.delete(url)

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)

    assert response_json_data['status_code'] == 200
    assert response_json_data['status'] == "Success"
    assert response_json_data['deleted_count'] == 1
    assert not Event.objects.filter(title="Test123 Event Title").exists()

@pytest.mark.django_db
def test_delete_event_user_not_exist(client, user, jwt_setup, event_id):
    """
    Test to delete an event of the current logged in user, but fail because the logged in user does not exist
    """
    test_create_event(client, user, jwt_setup, event_id)

    non_exist_user_jwt_response = jwt_handler("nonexist@gmail.com", "Non", "Exist", 809)
    non_exist_user_jwt_token = non_exist_user_jwt_response['jwt_token']
    client.cookies['jwt_token'] = non_exist_user_jwt_token

    url = reverse('Delete Event', kwargs = {'event_id': event_id[0] })
    response = client.delete(url)

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)

    assert response_json_data['status_code'] == 500
    assert response_json_data['description'] == "User does not exists in the database"

@pytest.mark.django_db
def test_delete_event_fail(client, user, jwt_setup, event_id):
    """
    Test to delete an event of the current logged in user, but fail because the event wanted to be deleted does not exist 
    """
    test_create_event(client, user, jwt_setup, event_id)

    url = reverse('Delete Event', kwargs = {'event_id': 712398 })
    response = client.delete(url)

    response_decoded_string = response.content.decode('utf-8')
    response_json_data = json.loads(response_decoded_string)

    assert response_json_data['status_code'] == 404
    assert response_json_data['status'] == "Failed"
    assert response_json_data['deleted_count'] == 0
    assert Event.objects.filter(title="Test123 Event Title").exists()

