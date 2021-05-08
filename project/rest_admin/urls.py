""" Rest Admin Router."""
""" Rest API Router. """
from django.urls import path, re_path

from rest_admin.src.modules.rest import views


app_name = "rest_admin"
urlpatterns = [
    # version 1
    path('healthcheck/ping', views.ping, name="ping")
    ]

