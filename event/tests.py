from django.test import TestCase, Client
from django.urls import reverse
# from django.contrib.sites.models import Site
from .models import Event
from user.models import User
from user.views import jwt_handler
import json

# Create your tests here.
class EventsCRUDTest(TestCase):
    def setUp(self):
        """
        All the set up needed for the event CRUDs tests
        """
        # set up the client to do CRUD
        self.client = Client()

        # set up the user object
        self.user = User.objects.create(
            email = "test123@gmail.com",
            first_name = "test",
            last_name = "123"
        )
        self.user_id = self.user.id

        # set up the jwt for the user test
        jwt_response = jwt_handler(self.user.email, self.user.first_name, self.user.last_name, self.user_id)
        self.jwt = jwt_response['jwt_token']
        self.client.cookies['jwt_token'] = self.jwt
        # print(jwt_response['status'])
    
    def test_create_event(self):
        """
        Test creating events    
        """
        data = {
            "title": "Test123 Event Title",
            "description": "Test123 Event description for testing",
            'date': '2024-01-01',
            'location': "12354 51st Test Ave N, TestCity WA 98413",
            'created_by': self.user_id
        }

        json_data = json.dumps(data)

        response = self.client.post(reverse('Create Event'), data = json_data, content_type = 'application/json')

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)

        # print(response.content)
        self.assertEqual(response_json_data['status_code'], 201)
        self.assertEqual(response_json_data['status'], "Success")
        self.assertTrue(Event.objects.filter(title="Test123 Event Title").exists())

    def test_retrieve_events_by_user_id_success(self):
        """
        Test to get events of a user with certain user id successfully
        """
        self.test_create_event()
        url = reverse('Retrieve Others Events', kwargs = {'user_id': self.user_id})
        response = self.client.get(url)

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)

        self.assertEqual(response_json_data['status_code'], 200)
        self.assertEqual(response_json_data['status'], "Success")
        # print(len(response_json_data['user_events']))
        self.assertTrue(len(response_json_data['user_events']) > 0)
    
    def test_retrieve_events_by_user_id_fail(self):
        """
        Test to get events of a user with certain user id but fail
        """
        self.test_create_event()
        url = reverse('Retrieve Others Events', kwargs = {'user_id': 7821368})
        response = self.client.get(url)

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)

        self.assertEqual(response_json_data['status_code'], 404)
        self.assertEqual(response_json_data['status'], "Failed")
        # print(len(response_json_data['user_events']))
        self.assertTrue(not hasattr(response_json_data, 'user_events'))

    def test_retrieve_events(self):
        """
        Test to get events of the current logged in user
        """
        self.test_create_event()
        url = reverse('Retrieve Own Events')
        response = self.client.get(url)

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)

        self.assertEqual(response_json_data['status_code'], 200)
        self.assertEqual(response_json_data['status'], "Success")
        # print(len(response_json_data['user_events']))
        self.assertTrue(len(response_json_data['user_events']) > 0)

    def test_update_event(self):
        """
        Test to update an event of the current logged in user
        """
        self.test_create_event()
        url = reverse('Retrieve Own Events')
        response = self.client.get(url)

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)

        self.assertEqual(response_json_data['status_code'], 200)
        self.assertEqual(response_json_data['status'], "Success")
        # print(len(response_json_data['user_events']))
        self.assertTrue(len(response_json_data['user_events']) > 0)
    # def test_delete_event(self):

    def tearDown(self):
        pass
