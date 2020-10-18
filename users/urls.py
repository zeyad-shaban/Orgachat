from . import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('', views.profile, name="profile"),
    path('all/', views.all_users, name='all_users'),
    path('add-friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('remove-friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
]