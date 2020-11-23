from . import views
from django.urls import path

app_name = 'chat'

urlpatterns = [
    path('friends/', views.friends_chat, name="friends"),
    path('groups/', views.groups_chat, name="groups"),
    path('get_chat/<int:chatId>/', views.get_chat, name='get_chat'),
    path('create_chat/', views.create_chat, name="create_chat"),
    path('add_member/', views.add_member, name='add_member'),
    path('groups/<int:chatId>/channels/create/', views.create_channel, name='create_channel'),
    path('groups/leave_group/<int:chatId>/', views.leave_group, name='leave_group'),
    path('groups/channels/toggle_mute_channel/<int:channelId>/', views.toggle_mute_channel, name='toggle_mute_channel')
]
