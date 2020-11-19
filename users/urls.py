from . import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    # ------------Users------------
    path('all/', views.all_users, name='all_users'),
    path('friends/', views.friends, name='friends'),
    path('update_account/', views.update_account, name='update_account'),
]
