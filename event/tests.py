from django.test import TestCase, Client
from django.urls import reverse
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

        self.assertEqual(response_json_data['status_code'], 201)
        self.assertEqual(response_json_data['status'], "Success")
        self.assertTrue(Event.objects.filter(title="Test123 Event Title").exists())
        self.event_id = Event.objects.filter(title="Test123 Event Title")[0].id

    def test_create_event_user_not_exists(self):
        """
        Test creating events, but fail because the logged in user does not exists 
        """
        data = {
            "title": "Test123 Event Title",
            "description": "Test123 Event description for testing",
            'date': '2024-01-01',
            'location': "12354 51st Test Ave N, TestCity WA 98413",
            'created_by': self.user_id
        }

        json_data = json.dumps(data)

        non_exist_user_jwt_response = jwt_handler("nonexist@gmail.com", "Non", "Exist", 809)
        self.jwt = non_exist_user_jwt_response['jwt_token']
        self.client.cookies['jwt_token'] = self.jwt
        
        response = self.client.post(reverse('Create Event'), data = json_data, content_type = 'application/json')

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)
        # print(response_json_data)

        self.assertEqual(response_json_data['status_code'], 401)
        self.assertEqual(response_json_data['description'], "User does not exists in the database")

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
        self.assertTrue(not hasattr(response_json_data, 'user_events'))

    def test_retrieve_events_by_user_id_user_not_exist(self):
        """
        Test to get events of a user with certain user id, but fail because the logged in user does not exist
        """
        self.test_create_event()
        
        non_exist_user_jwt_response = jwt_handler("nonexist@gmail.com", "Non", "Exist", 809)
        self.jwt = non_exist_user_jwt_response['jwt_token']
        self.client.cookies['jwt_token'] = self.jwt

        url = reverse('Retrieve Others Events', kwargs = {'user_id': self.user_id})
        response = self.client.get(url)

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)

        self.assertEqual(response_json_data['status_code'], 401)
        self.assertEqual(response_json_data['description'], "User does not exists in the database")

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
        self.assertTrue(len(response_json_data['user_events']) > 0)

    def test_retrieve_events_user_not_exist(self):
        """
        Test to get events of the current logged in user, but the logged in user does not exist
        """
        self.test_create_event()
        
        non_exist_user_jwt_response = jwt_handler("nonexist@gmail.com", "Non", "Exist", 809)
        self.jwt = non_exist_user_jwt_response['jwt_token']
        self.client.cookies['jwt_token'] = self.jwt

        url = reverse('Retrieve Own Events')
        response = self.client.get(url)

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)

        self.assertEqual(response_json_data['status_code'], 401)
        self.assertEqual(response_json_data['description'], "User does not exists in the database")

    def test_update_event_success(self):
        """
        Test to update an event of the current logged in user successfully
        """
        self.test_create_event()

        new_data = {
            "title": "Test123 Event New Title From Update",
            "description": "Test123 Event description for testing. This is the neew updated description",
            'date': '2024-02-02',
            'location': "51423 99st Test Ave W, TestCity WA 98413",
        }

        json_data = json.dumps(new_data)

        url = reverse('Update Event', kwargs = {'event_id': self.event_id })
        response = self.client.put(url, data = json_data, content_type = 'application/json')

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)

        self.assertEqual(response_json_data['status_code'], 200)
        self.assertEqual(response_json_data['status'], "Success")
        self.assertEqual(response_json_data['updated_count'], 1)
        self.assertTrue(Event.objects.filter(title="Test123 Event New Title From Update").exists())

    def test_update_event_user_not_exist(self):
        """
        Test to update an event of the current logged in user, but fail because the logged in user does not exists
        """
        self.test_create_event()

        new_data = {
            "title": "Test123 Event New Title From Update",
            "description": "Test123 Event description for testing. This is the neew updated description",
            'date': '2024-02-02',
            'location': "51423 99st Test Ave W, TestCity WA 98413",
        }

        json_data = json.dumps(new_data)

        non_exist_user_jwt_response = jwt_handler("nonexist@gmail.com", "Non", "Exist", 809)
        self.jwt = non_exist_user_jwt_response['jwt_token']
        self.client.cookies['jwt_token'] = self.jwt

        url = reverse('Update Event', kwargs = {'event_id': self.event_id })
        response = self.client.put(url, data = json_data, content_type = 'application/json')

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)

        self.assertEqual(response_json_data['status_code'], 401)
        self.assertEqual(response_json_data['description'], "User does not exists in the database")

    def test_update_event_fail(self):
        """
        Test to update an event of the current logged in user but fail because the id wanted to be updated does not exist
        """
        self.test_create_event()

        new_data = {
            "title": "Test123 Event New Title From Update",
            "description": "Test123 Event description for testing. This is the neew updated description",
            'date': '2024-02-02',
            'location': "51423 99st Test Ave W, TestCity WA 98413",
        }

        json_data = json.dumps(new_data)

        url = reverse('Update Event', kwargs = {'event_id': 300 })
        response = self.client.put(url, data = json_data, content_type = 'application/json')

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)

        self.assertEqual(response_json_data['status_code'], 404)
        self.assertEqual(response_json_data['status'], "Failed")
        self.assertEqual(response_json_data['updated_count'], 0)
        self.assertTrue(not Event.objects.filter(title="Test123 Event New Title From Update").exists())

    def test_delete_event_success(self):
        """
        Test to delete an event of the current logged in user successfully
        """
        self.test_create_event()

        url = reverse('Delete Event', kwargs = {'event_id': self.event_id })
        response = self.client.delete(url)

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)

        self.assertEqual(response_json_data['status_code'], 200)
        self.assertEqual(response_json_data['status'], "Success")
        self.assertEqual(response_json_data['deleted_count'], 1)
        self.assertTrue(not Event.objects.filter(title="Test123 Event Title").exists())

    def test_delete_event_user_not_exist(self):
        """
        Test to delete an event of the current logged in user, but fail because the logged in user does not exist
        """
        self.test_create_event()

        non_exist_user_jwt_response = jwt_handler("nonexist@gmail.com", "Non", "Exist", 809)
        self.jwt = non_exist_user_jwt_response['jwt_token']
        self.client.cookies['jwt_token'] = self.jwt

        url = reverse('Delete Event', kwargs = {'event_id': self.event_id })
        response = self.client.delete(url)

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)

        self.assertEqual(response_json_data['status_code'], 401)
        self.assertEqual(response_json_data['description'], "User does not exists in the database")

    def test_delete_event_fail(self):
        """
        Test to delete an event of the current logged in user, but fail because the event wanted to be deleted does not exist 
        """
        self.test_create_event()

        url = reverse('Delete Event', kwargs = {'event_id': 712398 })
        response = self.client.delete(url)

        response_decoded_string = response.content.decode('utf-8')
        response_json_data = json.loads(response_decoded_string)

        self.assertEqual(response_json_data['status_code'], 404)
        self.assertEqual(response_json_data['status'], "Failed")
        self.assertEqual(response_json_data['deleted_count'], 0)
        self.assertTrue(Event.objects.filter(title="Test123 Event Title").exists())

    def tearDown(self):
        pass
