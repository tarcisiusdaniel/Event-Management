from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.sites.models import Site
from unittest.mock import patch, MagicMock
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialLogin
# from django.contrib.auth import get_user_model 
from django.contrib.auth.models import User

from allauth.socialaccount.providers.google.provider import GoogleProvider

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
        self.user = User.objects.create_user(
            username = self.username,
            email = self.email,
            password = self.password,
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

    # Mock Google Callback and Test User Creation/Login
    # Mock of the post that can be done from user/login and test the redirect
    # @patch('allauth.socialaccount.providers.google.views.GoogleOAuth2Adapter.complete_login')
    # @patch('allauth.socialaccount.providers.google.views.GoogleOAuth2Adapter.get_provider')
    # def test_google_callback_success(self):
    #     """
    #     Test that the successful google callback creates a user and logs them in with redirecting to right url.
    #     """
    
    # def test_google_callback_failure(self):
    #     """
    #     Test that the unsuccessful google callback does not create a user.
    #     """

    def test_login_success(self):
        """
        Test to see if login successfully gives the right behavior (redirect to right url or not)
        This is also what happens after google callback being done after choosing the right google account
        """

        response = self.client.post(reverse('account_login'), {
            'login': self.username,
            'password': self.password
        })
        
        # print(response.content)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Login Handler'), status_code=302, target_status_code=200)

    def test_login_failure(self):
        """
        Test to see if login not successfully gives the right behavior (stay in the login page)
        """

        response = self.client.post(reverse('account_login'), {
            'login': self.username,
            'password': 'wrongpw'
        })
        
        # print(response.content)

        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        SocialApp.objects.all().delete()
        pass
