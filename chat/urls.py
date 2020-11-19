from . import views
from django.urls import path

app_name = 'chat'

urlpatterns = [
    path('friends/', views.friends_chat, name="friends"),
    path('groups/', views.groups_chat, name="groups"),
    path('get_chat/<int:chatId>/', views.get_chat, name='get_chat'),
    path('create_chat/', views.create_chat, name="create_chat"),
    path('send_text_message/', views.send_text_message, name='send_text_message'),
    path('add_member/', views.add_member, name='add_member'),
    path('groups/<int:chatId>/channels/create/', views.create_channel, name='create_channel'),
]
