from django.urls import path
from . import views

app_name="metrics"

urlpatterns = [
    path("", views.index, name="index"),
    path("growth_model/", views.growth_model, name="growth_model"),
]