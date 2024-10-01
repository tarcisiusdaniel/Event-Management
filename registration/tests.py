from django.test import TestCase, Client
from django.urls import reverse
from event.models import Event
from user.models import User
from .models import Registration
from user.views import jwt_handler
import json

# Create your tests here.
class RegistrationTest(TestCase):
    def setUp(self):
        """
        Necessary set up for the tests
        """
        # set up the client to do CRUD
        self.client = Client()

        # set up the user
        # the client will be later to have the same creds as this user object
        self.user = User.objects.create(
            email = "test123@gmail.com",
            first_name = "test",
            last_name = "123"
        )
        self.user_id = self.user.id

        # set up the event
        self.user_event = Event.objects.create(
            title = "The Title for Test123 Event",
            description = "This is the test description for Test123 event. Testing purposes",
            date = "2024-10-12",
            location = "9999 51st Ave W, TestCity, WA 98012",
            created_by = self.user,
        )
        self.user_event_id = self.user_event.id

        # set up the user's jwt in the cookie
        jwt_response = jwt_handler(self.user.email, self.user.first_name, self.user.last_name, self.user_id)
        self.jwt = jwt_response['jwt_token']
        self.client.cookies['jwt_token'] = self.jwt

    def test_register_user_to_event_success(self):
        """
        Test registering the logged in user to an event successfully
        """
        url = reverse('Register User to an Event', kwargs = {'event_id': self.user_event_id})
        response = self.client.post(url)

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)
        
        self.assertEqual(response_json_data['status_code'], 200)
        self.assertEqual(response_json_data['status'], "Success")
        self.assertTrue(Registration.objects.filter(user = self.user_id, event = self.user_event_id))

    def test_register_user_to_event_user_not_exist(self):
        """
        Test registering the logged in user to an event, but fail because the event does not exist
        """
        non_exist_user_jwt_response = jwt_handler("nonexist@gmail.com", "Non", "Exist", 809)
        self.jwt = non_exist_user_jwt_response['jwt_token']
        self.client.cookies['jwt_token'] = self.jwt

        url = reverse('Register User to an Event', kwargs = {'event_id': 2141})
        response = self.client.post(url)

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)
        
        self.assertEqual(response_json_data['status_code'], 401)
        self.assertEqual(response_json_data['description'], "User does not exists in the database")

    def test_register_user_to_event_fail(self):
        """
        Test registering the logged in user to an event, but fail because the event does not exist
        """
        url = reverse('Register User to an Event', kwargs = {'event_id': 2141})
        response = self.client.post(url)

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)
        
        self.assertEqual(response_json_data['status_code'], 404)
        self.assertEqual(response_json_data['status'], "Failed")
        self.assertEqual(response_json_data['description'], "Event does not exist")
        self.assertTrue(not Registration.objects.filter(user = self.user_id, event = self.user_event_id))
    
    def test_register_user_to_event_no_duplication(self):
        """
        Test registering the logged in user to an event, but fail because the event does not exist
        """
        self.test_register_user_to_event_success()
        url = reverse('Register User to an Event', kwargs = {'event_id': self.user_event_id})
        response = self.client.post(url)

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)
        
        self.assertEqual(response_json_data['status_code'], 202)
        self.assertEqual(response_json_data['status'], "No action")
        self.assertEqual(response_json_data['description'], "Registration not created. Already registered")
        self.assertTrue(len(Registration.objects.filter(user = self.user_id, event = self.user_event_id)) == 1)

    def tearDown(self):
        pass
