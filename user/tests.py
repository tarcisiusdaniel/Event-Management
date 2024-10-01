from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.sites.models import Site
from unittest.mock import patch, MagicMock
from allauth.socialaccount.models import SocialApp
from django.contrib.auth.models import User
from .models import User as U

import os
from dotenv import load_dotenv

load_dotenv()

# Create your tests here.
class GoogleSSOAuthenticationTest(TestCase):
    # setup testing environment
    # e.g.: creating users or initialize variables
    def setUp(self):
        self.client = Client()

        site, created = Site.objects.get_or_create(id=1, defaults={
            'domain': 'localhost',
            'name': 'localhost'
        })

        # print(os.getenv('GOOGLE_OAUTH_CLIENT_ID'))
        # print(os.getenv('GOOGLE_OAUTH_CLIENT_SECRET'))
        self.google_app = SocialApp.objects.create(
            provider = 'google',
            name = 'Google SSO',
            client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID'),
            secret = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
        )

        self.google_app.sites.add(1)  # Associate with the site

        # mock the user that can be used to log in
        self.username = 'test'
        self.email = 'test@mail.com'
        self.password = "efgh4321"
        self.first_name = "Test"
        self.last_name = "123"
        self.user = User.objects.create_user(
            username = self.username,
            email = self.email,
            password = self.password,
            first_name = self.first_name,
            last_name = self.last_name,
        )

        self.google_login_url = reverse('google_login')
        self.google_callback_url = reverse('google_callback')


    # Test to make sure if redirect to google for authentication is successful
    # Make sure the code redirects to google sso when trying to access google login
    def test_redirect_to_google(self):
        """
        Test if the user is redirected to google sso page for authentication
        """
        response = self.client.post(self.google_login_url)
        # print(response)

        # check if the response redirects to a URL
        self.assertEqual(response.status_code, 302)

        # check if the redirect URL has Google OAuth's URL
        self.assertTrue(response.url.startswith('https://accounts.google.com/o/oauth2/v2/'))

    def test_login_success(self):
        """
        Test to see if login successfully gives the right behavior (redirect to right url or not)
        This is also what happens after google callback being done after choosing the right google account
        """
        self.client.login(
            username = self.username,
            password = self.password
        )

        response = self.client.get(reverse('Login Handler'))
        # print(response.cookies['jwt_token'].value)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(U.objects.filter(email = self.email, first_name = self.first_name, last_name = self.last_name)) == 1)
        self.assertTrue(self.client.cookies['jwt_token'].value != "")

    def test_login_failure(self):
        """
        Test to see if login not successfully gives the right behavior (stay in the login page)
        """
        self.user.email = ""
        self.user.first_name = ""
        self.user.last_name = ""
        self.user.save()

        self.client.login(
            username = self.username,
            password = self.password
        )

        response = self.client.get(reverse('Login Handler'))

        self.assertEqual(response.status_code, 200)
    
    def test_login_success_without_creating_user(self):
        """
        Test to see if login successfully gives the right behavior (redirect to right url or not)
        This is also what happens after google callback being done after choosing the right google account
        """
        self.test_login_success()
        # print(self.user.email)
        # print(self.user.first_name)
        # print(self.user.last_name)
        self.client.login(
            username = self.username,
            password = self.password
        )

        response = self.client.get(reverse('Login Handler'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(U.objects.filter(email = self.email, first_name = self.first_name, last_name = self.last_name)) == 1)

    def test_logout(self):
        response = self.client.get(reverse('Logout Handler'))

        # print(response.cookies['jwt_token'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.cookies['jwt_token'].value == "")
    
    def tearDown(self):
        # SocialApp.objects.all().delete()
        pass
