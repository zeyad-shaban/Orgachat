from . import views
from django.urls import path

app_name = 'chat'

urlpatterns = [
    path('room/<int:room_id>/', views.room, name='room'),
    path('create-area/<int:room_id>/', views.create_area, name='create_area'),
    path('mute-area/<int:area_id>/', views.mute_area, name='mute_area'),
]