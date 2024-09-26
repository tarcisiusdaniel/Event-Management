from django.urls import path
from . import views

# (the url path, what is executed from the url path, name of the url path)
urlpatterns = [
    path('', views.index, name = 'Hello world'),
    path('login', views.login_handler, name = "Login Handler"),
    path('logout', views.logout_handler, name = "Logout Handler"),
]