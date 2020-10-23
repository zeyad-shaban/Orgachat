from django.urls import path
from . import views

urlpatterns = [
    path("user_installed/", views.user_installed, name="user_installed")
]