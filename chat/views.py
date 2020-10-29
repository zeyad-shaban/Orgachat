import time
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import random
import logging
import json
from users.models import HomepageArea
from django.core.exceptions import PermissionDenied
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from chat.models import Area, Message, Room
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from webpush import send_user_notification
from django.contrib.auth.decorators import login_required
User = get_user_model()
logger = logging.getLogger('djpwa.pwa.views')


def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_rooms = Room.objects.filter(chatters=request.user)
            general_rooms = []
            for room in user_rooms:
                if room.homepage_area.count() <= 0 or not room.get_homepage_area():
                    general_rooms.append(room)

            general_count = 0
            for room in general_rooms:
                general_count += room.unread_count()
            if general_count <= 0:
                general_count = ''
            return render(request, 'chat/home.html', {'general_rooms': general_rooms, "general_count": general_count})

        else:
            messages.error(request, 'Please create an account or login first')
            return redirect('signupuser')


@login_required
def room(request, room_id, area_id=None):
    room = get_object_or_404(Room, pk=room_id)
    area_id = request.GET.get('area_id')
    if not area_id:
        area_id = json.loads(request.body).get('area_id')
    try:
        requestedPage = json.loads(request.body).get("page")
    except:
        requestedPage = None
    if request.method == 'GET' or requestedPage:
        users = room.chatters.all()
        users = []
        if not request.user in room.chatters.all():
            raise PermissionDenied
        for message in room.message_set.filter(Q(is_read=False), ~Q(user=request.user)):
            message.is_read = True
            message.save()

        room_messages_list = room.message_set.all()
        data = {'room': room, 'users': users}
        if area_id:
            area = get_object_or_404(Area, pk=area_id)
            room_messages_list = room.message_set.filter(area=area)
            data["area"] = area

        paginator = Paginator(room_messages_list, 20)
        page = requestedPage
        if not page:
            page = 1
        try:
            room_messages = paginator.page(paginator.num_pages - (page-1))
        except PageNotAnInteger:
            room_messages = paginator.page(paginator.num_pages)
        except EmptyPage:
            room_messages = []

        data["room_messages"] = room_messages
        if not requestedPage:
            return render(request, 'chat/room.html', data)
        else:
            json_messages = [message.json() for message in room_messages]
            return JsonResponse({"messages": json_messages})
    else:
        data = json.loads(request.body)
        area = get_object_or_404(Area, pk=data.get('area'))
        message = Message.objects.create(
            user=request.user, text=data.get('text'), room=room, area=area)
        message.save()
        # Web push
        payload = {"head": room.title(), "body": message.__str__(), "icon": "/static/chat/img/favicon.png",
                   "url": f"https://www.orgachat.com/chat/room/{room.id}/"}
        for chatter in room.chatters.all():
            if not chatter in message.area.muted_users.all() and chatter != request.user and (True):  # todo check for chatter url
                try:
                    send_user_notification(
                        user=chatter, payload=payload, ttl=1000)
                    print("SUCCESS TO SEND NOTIFICATIONS")
                except Exception as err:
                    print("Error: ", err)
        return redirect('chat:room', room_id=room_id)


@login_required
def save_file_message(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
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
    room = get_object_or_404(Room, pk=room_id)
    area = get_object_or_404(Area, pk=int(request.POST.get("area")))
    message = Message.objects.create(
        user=request.user, audio=request.FILES.get("audio"), room=room, area=area)
    message.save()
    return redirect("chat:room", room_id=room.id)


@login_required
def load_messages(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
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
    room = Room.objects.create(name=request.POST.get('name'), type='group')
    room.save()
    room.chatters.add(request.user)
    area = Area.objects.create(title='general', room=room)
    area.save()
    messages.success(request, 'Created successfully')
    return redirect('home')


def add_user(request, user_id, room_id):
    user = get_object_or_404(User, pk=user_id)
    room = get_object_or_404(Room, pk=room_id)
    room.chatters.add(user)
    return redirect('chat:room', room_id=room_id)


def remove_user(request, user_id, room_id):
    user = get_object_or_404(User, pk=user_id)
    room = get_object_or_404(Room, pk=room_id)
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
    room = get_object_or_404(Room, pk=room_id)
    if not request.user in room.chatters.all():
        raise PermissionDenied
    area = Area.objects.create(title=request.POST.get('title'), room=room)
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
    homepage_area = HomepageArea.objects.create(
        title=request.POST.get('title'), user=request.user)
    homepage_area.save()
    return redirect('home')


def move_room(request, homepage_area_id):
    try:
        homepage_area = get_object_or_404(HomepageArea, pk=homepage_area_id)
    except:
        homepage_area = None
    room_id = int(json.loads(request.body).get("room_id"))
    room = get_object_or_404(Room, pk=room_id)
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
