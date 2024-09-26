from django.urls import path
from . import views

# (the url path, what is executed from the url path, name of the url path)
urlpatterns = [
    path('', views.index, name = 'hello world'),
]