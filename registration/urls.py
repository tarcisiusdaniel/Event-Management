from django.urls import path
from . import views

# (the url path, what is executed from the url path, name of the url path)
urlpatterns = [
    path('', views.index, name = 'Hello world'),
    path('register/event/id/<int:event_id>', views.register_user_to_event, name='Register User to an Event')
]