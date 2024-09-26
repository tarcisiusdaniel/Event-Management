from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# how to get the info saved in the email used
def index(request):
    print("Hello")
    return HttpResponse("Hello, World!")