from django.views.decorators.csrf import csrf_exempt
import json
from users.serializers import UserSerializer
from django.core.serializers import serialize
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.db.models.query_utils import Q
from chat.models import Channel,  Chat, Message
from .serializers import MessageSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def friends_chat(request):
    request.user.update_last_seen()
    friend_chats = Chat.objects.filter(
        chatters=request.user, type='friend', is_deleted=False, is_archived=False)
    chats = [chat.to_json_preview() for chat in friend_chats.all()]

    return Response(list(chats))


@api_view(('GET', 'POST'))
@permission_classes([IsAuthenticated, ])
def groups_chat(request):
    request.user.update_last_seen()
    if request.method == 'GET':
        group_chats = Chat.objects.filter(
            chatters=request.user, type='group', is_archived=False)
        chats = [chat.to_json_preview() for chat in group_chats.all()]
        return Response(list(chats))
    else:
        chat = Chat.objects.create(
            title=request.data.get('title'), type="group")
        chat.chatters.add(request.user)
        Channel.objects.create(title="general", chat=chat)

        return Response({"message": "Successfully created the group"}, status.HTTP_200_OK)


@api_view(('GET', 'POST'))
@permission_classes([IsAuthenticated])
def create_chat(request):
    request.user.update_last_seen()
    friend = get_object_or_404(User, pk=request.data.get("friendId"))
    if request.user.id == friend.id:
        return Response({'error': "You can't chat with yourself"}, status.HTTP_400_BAD_REQUEST)

    chat = Chat.objects.filter(type=f'friend', chatters=request.user).filter(
        chatters=friend).first()
    if not chat:
        chat = Chat.objects.create(type='friend')
        chat.chatters.add(request.user)
        chat.chatters.add(friend)
    if not friend in request.user.friends.all():
        request.user.friends.add(friend)
        friend.friends.add(request.user)

    return Response({'chat': chat.to_json_preview(), 'messages': serialize('json', chat.message_set.all())})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat(request, chatId):
    request.user.update_last_seen()
    chat = get_object_or_404(Chat, pk=chatId)
    if not request.user in chat.chatters.all():
        return Response({"Error": 'You don\'t belong to this chat'}, status.HTTP_401_UNAUTHORIZED)

    channel = chat.get_channel(request.GET.get('channelId'))

    if chat.type == 'group':
        json_chat = chat.to_json(channel)
        json_chat['channel'] = channel.to_json()
        [message.read_users.add(request.user) for message in chat.message_set.filter(
            ~Q(read_users=request.user), Q(channel=channel))]

    else:
        [message.read_users.add(request.user) for message in chat.message_set.filter(
            ~Q(read_users=request.user))]
        json_chat = chat.to_json()
    return Response({'chat': json_chat, 'messages': json_chat['messages']}, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request, chatId, type):
    request.user.update_last_seen()
    chat = get_object_or_404(Chat, pk=chatId)
    channel = chat.get_channel(request.GET.get('channelId'))
    file = request.FILES.get('file')

    message = Message.objects.create(
        chat=chat, user=request.user, channel=channel)

    if type == 'image':
        message.image = file
    elif type == 'video':
        message.video = file
    elif type == 'audio':
        message.audio = file

    message.save()
    return Response(message.to_json(), status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def add_member(request):
    request.user.update_last_seen()
    data = request.data.get('userId')
    chat = get_object_or_404(Chat, pk=data.get('chatId'))
    if not data.get('userId'):
        # todo show users who are not in the group
        q = request.GET.get("q")
        if q:
            users_list = User.objects.filter(Q(username__icontains=q) | Q(
                email__icontains=q)).order_by("-friends")
        else:
            users_list = User.objects.filter(
                ~Q(id=request.user.id)).order_by("-friends")

        return Response([user.to_json() for user in users_list if not user in chat.chatters.all()])
    else:
        user = get_object_or_404(User, pk=data.get('userId'))
        if not user in chat.chatters.all():
            chat.chatters.add(user)
        # Todo check if user doesn't allow anyone to add him to the group
        return Response({"message": "added"}, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def create_channel(request, chatId):
    request.user.update_last_seen()
    chat = get_object_or_404(Chat, pk=chatId)
    channel = Channel.objects.create(
        title=request.data.get('title'), chat=chat)
    return Response({'channel': channel.to_json()}, status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def toggle_mute_channel(request, channelId):
    request.user.update_last_seen()
    channel = get_object_or_404(Channel, pk=channelId)
    if request.user in channel.muted_users.all():
        channel.muted_users.remove(request.user)
    else:
        channel.muted_users.add(request.user)

    return Response({'channel': channel.to_json()}, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def leave_group(request, chatId):
    request.user.update_last_seen()
    chat = get_object_or_404(Chat, pk=chatId)
    if request.user in chat.chatters.all():
        chat.chatters.remove(request.user)
    if chat.chatters.count() <= 0:
        chat.delete()
    return Response({'message': 'successfully left the group'}, status.HTTP_200_OK)
