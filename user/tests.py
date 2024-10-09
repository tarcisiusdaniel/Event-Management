from django.test import Client
from django.urls import reverse

import pytest
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.contrib.auth.models import User
from .models import User as U
from .views import get_parameter

from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def client():
    """
    Set up client
    """
    return Client()

@pytest.fixture
def site():
    """
    Set up site
    """
    site, created = Site.objects.get_or_create(id = 1, defaults={
        'domain': 'localhost',
        'name': 'localhost'
    })
    return site

@pytest.fixture
def google_app(site):
    """
    Set up Google application
    """
    google_app = SocialApp.objects.create(
        provider = 'google',
        name = 'Google SSO',
        client_id = get_parameter('/event_management_backend/GOOGLE_OAUTH_CLIENT_ID'),
        secret = get_parameter('/event_management_backend/GOOGLE_OAUTH_CLIENT_SECRET')
    )
    google_app.sites.add(1)
    return google_app

@pytest.fixture
def user():
    """
    Set up User that is logged in
    """
    username = 'test'
    email = 'test@mail.com'
    password = "efgh4321"
    first_name = "Test"
    last_name = "123"
    user = User.objects.create_user(
        username = username,
        email = email,
        password = password,
        first_name = first_name,
        last_name = last_name,
    )
    return user

@pytest.fixture
def google_urls():
    """
    Set up the urls for Google SSO
    """
    return {
        "login": reverse('google_login'),
        "callback": reverse('google_callback'),
    }

@pytest.fixture
def user_urls():
    """
    Set up urls for user app
    """
    return {
        "login": reverse('Login Handler'),
        "logout": reverse('Logout Handler'),
    }

@pytest.mark.django_db
def test_redirect_to_google(client, google_app, google_urls):
    """
    Test if the user is redirected to google sso page for authentication
    """
    response = client.post(google_urls['login'])
    # print(response)

    assert response.status_code == 302

    assert response.url.startswith('https://accounts.google.com/o/oauth2/v2/')

@pytest.mark.django_db
def test_login_success(client, user, user_urls):
    """
    Test to see if login successfully gives the right behavior (redirect to right url or not)
    This is also what happens after google callback being done after choosing the right google account
    """
    username = 'test'
    email = 'test@mail.com'
    password = "efgh4321"
    first_name = "Test"
    last_name = "123"
    client.login(
        username = username,
        password = password
    )

    response = client.get(user_urls["login"])
    # print(response.cookies['jwt_token'].value)

    assert response.status_code == 200
    assert len(U.objects.filter(
        email = email, 
        first_name = first_name, 
        last_name = last_name)
        ) == 1
    assert client.cookies['jwt_token'].value != ""

@pytest.mark.django_db
def test_login_failure(client, user, user_urls):
    """
    Test to see if login not successfully gives the right behavior (stay in the login page)
    """
    username = 'test'
    email = 'test@mail.com'
    password = "efgh4321"
    first_name = "Test"
    last_name = "123"

    user_figure = user
    user_figure.email = ""
    user_figure.first_name = ""
    user_figure.last_name = ""
    user_figure.save()

    client.login(
        username = username,
        password = password
    )

    response = client.get(user_urls["login"])

    ######## fix this one, should give an error message
    # self.assertEqual(response.status_code, 500) 
    
@pytest.mark.django_db
def test_login_success_without_creating_user(client, user, user_urls):
    """
    Test to see if login successfully gives the right behavior (redirect to right url or not)
    This is also what happens after google callback being done after choosing the right google account
    """
    test_login_success(client, user, user_urls)

    username = 'test'
    email = 'test@mail.com'
    password = "efgh4321"
    first_name = "Test"
    last_name = "123"

    client.login(
        username = username,
        password = password
    )

    response = client.get(user_urls["login"])

    assert response.status_code == 200
    assert len(U.objects.filter(
        email = email, 
        first_name = first_name, 
        last_name = last_name)
        ) == 1

@pytest.mark.django_db
def test_logout(client, user, user_urls):
    """
    Test logging out
    """
    response = client.get(user_urls["logout"])

    # print(response.cookies['jwt_token'])
    assert response.status_code == 200
    assert response.cookies['jwt_token'].value == ""
