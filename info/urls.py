from django.urls import path
from . import views
app_name = 'info'

urlpatterns = [
    path("termsandconditions/", views.termsandconditions, name="termsandconditions"),
    path("privacypolicy/", views.privacypolicy, name="privacypolicy"),
    path("cookiepolicy/", views.cookiepolicy, name="cookiepolicy"),
]
