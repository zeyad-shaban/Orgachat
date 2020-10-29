from django.urls import path
from . import views

app_name="metrics"

urlpatterns = [
    path("", views.index, name="index"),
    path("growth_model/", views.growth_model, name="growth_model"),
    path("user_installed/", views.user_installed, name="user_installed"),
]