from . import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    # ------------Users------------
    path('', views.profile, name="profile"),
    path('view/<int:user_id>/', views.view_user, name="view_user"),
    path('all/', views.all_users, name='all_users'),
    path('friends/', views.friends, name='friends'),
]
