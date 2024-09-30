from django.urls import path
from . import views

# (the url path, what is executed from the url path, name of the url path)
urlpatterns = [
    path('', views.index, name = 'Hello world'),
    path('create', views.create_event, name = "Create Event"),
    path('retrieve/id/<int:user_id>', views.retrieve_events_by_user_id, name = "Retrieve Others Events"),
    path('retrieve/', views.retrieve_events, name = "Retrieve Own Events"),
    path('update/id/<int:event_id>', views.update_event, name = "Update Event"),
    path('delete/id/<int:event_id>', views.delete_event, name = "Delete Event"),
]
