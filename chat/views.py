from users.serializers import UserSerializer
from django.core.serializers import serialize
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from chat.serializers import ChatSerializer, MessageSerializer
from django.db.models.query_utils import Q
from chat.models import Channel, Message, Chat
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def friends_chat(request):
    friend_chats = Chat.objects.filter(
        chatters=request.user, type='friend', is_deleted=False, is_archived=False)
    chats = [chat.to_json_preview() for chat in friend_chats.all()]

    return Response(list(chats))


@api_view(('GET', 'POST'))
@permission_classes([IsAuthenticated, ])
def groups_chat(request):
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
    chat = get_object_or_404(Chat, pk=chatId)
    if not request.user in chat.chatters.all():
        return Response({"Error": 'You don\'t belong to this chat'}, status.HTTP_401_UNAUTHORIZED)

    if chat.type == 'group':
        try:
            channelId = int(request.GET.get('channelId'))
            channel = get_object_or_404(Channel, pk=channelId)
        except:
            try:
                channel = chat.channel_set.first()
            except:
                channel = None
        json_chat = chat.to_json(channel)
        if channel:
            json_chat['channel'] = channel.to_json()
        else:
            json_chat['channel'] = channel

    else:
        json_chat = chat.to_json()
    return Response(json_chat, status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated, ])
def send_text_message(request):
    serializer = MessageSerializer(data=request.data)
    chat = get_object_or_404(Chat, pk=serializer.initial_data['chatId'])
    try:
        channel = get_object_or_404(
            Chat, pk=serializer.initial_data["areaId"])
    except Exception as error:
        channel = None
    text = serializer.initial_data['text']
    if text.replace(" ", "") == "":
        return Response({"error": "Text must be 1 character at least"}, status.HTTP_400_BAD_REQUEST)
    message = Message.objects.create(
        user=request.user, text=text, chat=chat, channel=channel)
    message.save()
    return Response()


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def add_member(request):
    data = request.data.get('userId')
    chat = get_object_or_404(Chat, pk=data.get('chatId'))
    if not data.get('userId'):
        # todo show users who are not in the group
        q = request.GET.get("q")
        if q:
            users_list = User.objects.filter(Q(username__icontains=q) | Q(
                email__icontains=q) | Q(country__icontains=q)).order_by("-friends")
        else:
            users_list = User.objects.filter(
                ~Q(id=request.user.id)).order_by("-friends")

        users = [user for user in users_list if not user in chat.chatters.all()]

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    else:
        user = get_object_or_404(User, pk=data.get('userId'))
        if not user in chat.chatters.all():
            chat.chatters.add(user)
        # Todo check if user doesn't allow anyone to add him to the group
        return Response({"message": "added"}, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def create_channel(request, chatId):
    chat = get_object_or_404(Chat, pk=chatId)
    channel = Channel.objects.create(
        title=request.data.get('title'), chat=chat)
    return Response({'channel': channel.to_json()}, status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def leave_group(request, chatId):
    chat = get_object_or_404(Chat, pk=chatId)
    if request.user in chat.chatters.all():
        chat.chatters.remove(request.user)
    return Response({'message': 'successfully removed from the group'}, status.HTTP_200_OK)