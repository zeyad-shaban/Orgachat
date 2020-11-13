from . import views
from django.urls import path

app_name = 'chat'

urlpatterns = [
     path('friends/', views.friends_chat, name="friends"),
     path('groups/', views.groups_chat, name="groups"),
    path('room/<int:room_id>/', views.room,
         kwargs={'area_id': None}, name='room'),
    path('load_messages/<int:room_id>/',
         views.load_messages, name='load_messages'),

    path('save_file_message/<int:room_id>/',
         views.save_file_message, name="save_file_message"),
    path('save_file_message/<int:room_id>/',
         views.save_file_message, name="save_file_message"),
    path('record_audio_message/<int:room_id>/',
         views.record_audio_message, name="record_audio_message"),
    # Group
    path('create-group/', views.create_group, name="create_group"),
    path('add-user/<int:user_id>/<int:room_id>/',
         views.add_user, name='add_user'),
    path('remove-user/<int:user_id>/<int:room_id>/',
         views.remove_user, name='remove_user'),
    # Areas
    path('create-area/<int:room_id>/', views.create_area, name='create_area'),
    path('mute-area/<int:area_id>/', views.mute_area, name='mute_area'),
    #     Homepage areas
    path('create-homepage-area/', views.create_homepage_area, name='create_homepage_area'),
    path('move_room/<int:homepage_area_id>/', views.move_room, name='move_room'),
    # Stars
    path('star-area/<int:area_id>/', views.star_area, name='star_area'),
]
