from . import views
from django.urls import path

app_name = 'chat'

urlpatterns = [
    path('room/<int:room_id>/', views.room,
         kwargs={'area_id': None}, name='room'),
    path('load_messages/<int:room_id>/', views.load_messages, name='load_messages'),
    # Areas
    path('create-area/<int:room_id>/', views.create_area, name='create_area'),
    path('mute-area/<int:area_id>/', views.mute_area, name='mute_area'),
    # Stars
    path('star-area/<int:area_id>/', views.star_area, name='star_area'),
]
