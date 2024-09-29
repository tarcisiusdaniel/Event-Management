from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import User
import jwt, datetime, json
import os
from dotenv import load_dotenv


load_dotenv()

# Create your views here.
def index(request):
    return HttpResponse('Hello World')

# @login_required
def login_handler(request):
    """
    Handling login using any kind of method (Google SSO, normal sign in, etc.)
    """
    email = ""
    first_name = ""
    last_name = ""
    if request.body:
        decoded_string = request.body.decode('utf-8')
        json_data = json.loads(decoded_string)
        email = json_data['user']['email']
        first_name = json_data['user']['first_name']
        last_name = json_data['user']['last_name']
    
    # this can come from sso
    elif request.user:
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name

    if email != "" and first_name != "" and last_name != "":
        # create the user
        # code right here to create the user and store it in postgresql table
        # also, make the session for the sign-in
        # use jwt
        # create the jwt, and use it for accessing all the services later on

        sign_in_json_response = user_sign_in_handler(email, first_name, last_name)
        # print(response)
        jwt_response = jwt_handler(email, first_name, last_name)

        # if the sign in and making jwt are success
        if sign_in_json_response['status'] == 'Success' and jwt_response['status'] == 'Success':
            response_data = {
                'status': "Login Success",
                'jwt_token': jwt_response['jwt_token'],
            }
            response = JsonResponse(response_data)
            response.set_cookie(key='jwt_token', value = jwt_response['jwt_token'], httponly=True)
            return response

            # return HttpResponse('Login Success. JWT Token, ' + f'${jwt_response['jwt_token']}')

        # if fail
    return Response({
        'status': 'Login Fail'
    })

    # return HttpResponse('Login Fail')
        

def user_sign_in_handler(email, first_name, last_name):
    """
    Handling user creation upon login
    """
    if email == '':
        return {
            'status': 'Fail',
            'description': 'Email does not exist',
        }
    response = ""
    try :
        tuple = User.objects.get(email = email, first_name = first_name, last_name = last_name)
        response = "Tuple already exist. Signing in, but not making new tuple"
    except User.DoesNotExist :
        new_tuple = User(email = email, first_name = first_name, last_name = last_name)
        new_tuple.save()
        response = "Tuple does not exist. Signing in and making new tuple"
    return {
        'status': 'Success',
        'description': response,
    }

def jwt_handler(email, first_name, last_name):
    """
    Handling JWT for authentication. Put the  
    """
    if email == '':
        return {
            'status': 'Fail',
            'description': 'Email does not exist',
        }
    payload = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')
    return {
        'status': 'Success',
        'jwt_token': token,
    }

def user_auth_jwt(request):
    """
    Authenticate user with the JWT
    """
    token = request.COOKIES.get('jwt_token')
    print(token)
    if not token:
        return JsonResponse({
            'status': "Failed",
            'description': "Token is invalid"
        })
    
    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
        tuple = User.objects.get(email = payload['email'], first_name = payload['first_name'], last_name = payload['last_name'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({
            'status': "Failed",
            'description': "Token Expired"
        })
    except User.DoesNotExist:
        return JsonResponse({
            'status': "Failed",
            'description': "User does not exists in the database"
        })

    return JsonResponse({
        'status': "Success",
        'description': "User is authenticated"
    })


def logout_handler(request):
    """
    Handling log out
    """
    return HttpResponse("Bye")