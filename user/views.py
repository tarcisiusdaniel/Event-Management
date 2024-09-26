from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return HttpResponse('Hello World')

@login_required
def login_handler(request):
    email = request.user.email
    first_name = request.user.first_name
    last_name = request.user.last_name
    print(first_name + " " + last_name)

    ##################################
    # create the user
    # code right here to create the user and store it in postgresql table

    # also, handle if there is already an account with the google email
    ##################################

    return HttpResponse('Hello, ' + f'{email}')

def logout_handler(request):
    return HttpResponse("Bye")