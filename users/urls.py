from . import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    # ------------Users------------
    path('all/', views.all_users, name='all_users'),
    path('friends/', views.friends, name='friends'),
    path('update_account/', views.update_account, name='update_account'),
    path('save_expo_push_token/', views.save_expo_push_token, name='save_expo_push_token'),
    path('update_last_seen/', views.update_last_seen, name='update_last_seen')
]
