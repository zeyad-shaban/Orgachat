from django.core.serializers import serialize
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from chat.serializers import ChatSerializer, MessageSerializer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json
from users.models import Category
from django.core.exceptions import PermissionDenied
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from chat.models import Area, Message, Chat
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
User = get_user_model()


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def friends_chat(request):
    friend_chats = Chat.objects.filter(chatters=request.user, type='friend', is_deleted=False, is_archived=False)
    chats = [chat.to_json() for chat in friend_chats.all()]

    return Response(list(chats))


@api_view(('GET', 'POST'))
@permission_classes([IsAuthenticated, ])
def groups_chat(request):
    if request.method == 'GET':
        group_chats = Chat.objects.filter(chatters=request.user, type='group', is_archived=False)
        chats = [chat.to_json() for chat in group_chats.all()]
        return Response(list(chats))
    else:
        # todo create a group
        pass


@api_view(('GET', 'POST'))
@permission_classes([IsAuthenticated])
def get_chat(request):
    serializer = ChatSerializer(data=request.data)

    type = serializer.initial_data["type"]
    if type == "friend" or not type:
        friend = get_object_or_404(
            User, pk=serializer.initial_data["friendId"])

        if request.user.id == friend.id:
            return Response({'error': "You can't chat with yourself"}, status.HTTP_400_BAD_REQUEST)

        chats = Chat.objects.filter(type=type, chatters=request.user)
        chat = None
        for chat in chats:
            if friend in chat.chatters.all():
                chat = chat
        if not chat:
            chat = Chat.objects.create(type=serializer.initial_data["type"])
            chat.chatters.add(request.user)
            chat.chatters.add(friend)
    else:
        chat = get_object_or_404(Chat, pk=serializer.initial_data["chatId"])
    return Response({'chat': chat.to_json(), 'messages': serialize('json', chat.message_set.all())})


@api_view(["POST"])
@permission_classes([IsAuthenticated, ])
def send_text_message(request):
    serializer = MessageSerializer(data=request.data)
    chat = get_object_or_404(Chat, pk=serializer.initial_data['chatId'])
    try:
        area = get_object_or_404(
            Chat, pk=serializer.initial_data["areaId"])
    except Exception as error:
        area = None
    text = serializer.initial_data['text']
    if text.replace(" ", "") == "":
        return Response({"error": "Text must be 1 character at least"}, status.HTTP_400_BAD_REQUEST)
    message = Message.objects.create(
        user=request.user, text=text, chat=chat, area=area)
    message.save()
    return Response()


@api_view(["POST"])
@permission_classes([IsAuthenticated, ])
def get_messages(request):
    pass


@login_required
def save_file_message(request, room_id):
    room = get_object_or_404(Chat, pk=room_id)
    area = get_object_or_404(Area, pk=int(request.POST.get('area')))

    if request.FILES.get("video"):
        for video in request.FILES.getlist("video"):
            message = Message.objects.create(
                user=request.user, video=video, room=room, area=area)
            message.save()
    elif request.FILES.get("image"):
        for image in request.FILES.getlist("image"):
            message = Message.objects.create(
                user=request.user, image=image, room=room, area=area)
            message.save()
    elif request.FILES.get("file"):
        for file in request.FILES.getlist("file"):
            message = Message.objects.create(
                user=request.user, file=file, room=room, area=area)
            message.save()
    elif request.FILES.get("audio"):
        for audio in request.FILES.getlist("audio"):
            message = Message.objects.create(
                user=request.user, audio=audio, room=room, area=area)
            message.save()
    return redirect("chat:room", room_id=room.id)


@login_required
def record_audio_message(request, room_id):
    room = get_object_or_404(Chat, pk=room_id)
    area = get_object_or_404(Area, pk=int(request.POST.get("area")))
    message = Message.objects.create(
        user=request.user, audio=request.FILES.get("audio"), room=room, area=area)
    message.save()
    return redirect("chat:room", room_id=room.id)


@login_required
def load_messages(request, room_id):
    room = get_object_or_404(Chat, pk=room_id)
    if not request.user in room.chatters.all():
        raise PermissionDenied
    data = json.loads(request.body)
    if not data.get('area_id'):
        new_messages = room.message_set.filter(
            ~Q(user=request.user), Q(id__gt=data.get('last_id')))
    else:
        area = get_object_or_404(Area, pk=data.get('area_id'))
        new_messages = room.message_set.filter(
            ~Q(user=request.user), Q(id__gt=data.get('last_id')), Q(area=area))
    json_new_messages = [message.json() for message in new_messages]
    return JsonResponse({'new_messages': json_new_messages})


# --------Group------------
def create_group(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login to continue")
        return redirect("signupuser")
    room = Chat.objects.create(name=request.POST.get('name'), type='group')
    room.save()
    room.chatters.add(request.user)
    area = Area.objects.create(title='general', room=room)
    area.save()
    messages.success(request, 'Created successfully')
    return redirect('home')


def add_user(request, user_id, room_id):
    user = get_object_or_404(User, pk=user_id)
    room = get_object_or_404(Chat, pk=room_id)
    room.chatters.add(user)
    return redirect('chat:room', room_id=room_id)


def remove_user(request, user_id, room_id):
    user = get_object_or_404(User, pk=user_id)
    room = get_object_or_404(Chat, pk=room_id)
    room.chatters.remove(user)
    room.homepage_area.remove(room.get_homepage_area())
    message = Message.objects.create(
        room=room, text=f"{request.user.username} removed {user.username}", user=request.user)
    message.save()
    if room.chatters.count() <= 0:
        room.delete()
    if user == request.user:
        return redirect('home')
    else:
        return redirect('chat:room', room_id=room_id)

# ----------Area------------


@login_required
def create_area(request, room_id):
    room = get_object_or_404(Chat, pk=room_id)
    if not request.user in room.chatters.all():
        raise PermissionDenied
    title = json.loads(request.body).get('title')
    area = Area.objects.create(title=title, room=room)
    area.save()
    messages.success(request, 'Successfully created area')
    return redirect('chat:room', room_id=room.id)


def mute_area(request, area_id):
    area = get_object_or_404(Area, pk=area_id)
    if request.user in area.muted_users.all():
        area.muted_users.remove(request.user)
    else:
        area.muted_users.add(request.user)
    return redirect('chat:room', area.room.id)

# ---------Homepage Areas-------------


def create_homepage_area(request):
    homepage_area = Category.objects.create(
        title=request.POST.get('title'), user=request.user)
    homepage_area.save()
    return redirect('home')


def move_room(request, homepage_area_id):
    try:
        homepage_area = get_object_or_404(Category, pk=homepage_area_id)
    except:
        homepage_area = None
    room_id = int(json.loads(request.body).get("room_id"))
    room = get_object_or_404(Chat, pk=room_id)
    curr_area = room.get_homepage_area()
    room.homepage_area.remove(curr_area)
    room.homepage_area.add(homepage_area)
    room.save()
    return redirect('home')

# --------------Star-----------------


def star_area(request, area_id):
    area = get_object_or_404(Area, pk=area_id)
    if request.user in area.star_users.all():
        area.star_users.remove(request.user)
    else:
        for aarea in area.room.area_set.all():
            if request.user in aarea.star_users.all():
                aarea.star_users.remove(request.user)
        area.star_users.add(request.user)
    return redirect('chat:room', area.room.id)
