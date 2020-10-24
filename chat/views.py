import json
from users.models import HomepageArea
from django.core.exceptions import PermissionDenied
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from chat.models import Area, Message, Room
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from webpush import send_user_notification
User = get_user_model()
import logging
import random
import time
logger = logging.getLogger('djpwa.pwa.views')


# Service worker
def random_response(request):
    response_time_ms = random.choice((0, 10, 50, 100, 1_000, 10_000))
    response_time = response_time_ms / 1_000
    print(f'Selected response time {response_time}')
    time.sleep(response_time)
    return render(request, 'chat/random_response.html', context={'response_time': response_time})



# End service worker

def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            unorganized_rooms = Room.objects.filter(chatters=request.user, homepage_area=None)
            return render(request, 'chat/home.html', {'unorganized_rooms': unorganized_rooms})
        else:
            messages.error(request, 'Please create an account or login first')
            return redirect('signupuser')


@login_required
def room(request, room_id, area_id=None):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'GET':
        all_users = User.objects.filter(~Q(id=request.user.id))
        users = []
        for user in all_users:
            if not user in room.chatters.all():
                users.append(user)

        if not request.user in room.chatters.all():
            raise PermissionDenied
        for message in room.message_set.all():
            if message.user != request.user:
                message.is_read = True
                message.save()

        room_messages = room.message_set.all()
        if request.GET.get('area_id'):
            area = get_object_or_404(Area, pk=request.GET.get('area_id'))
            room_messages = room.message_set.filter(area=area)
        return render(request, 'chat/room.html', {'room': room, 'room_messages': room_messages, 'users': users, })
    else:
        data = json.loads(request.body)
        area = get_object_or_404(Area, pk=data.get('area'))
        message = Message.objects.create(
            user=request.user, text=data.get('text'), room=room, area=area)
        message.save()
        # Web push
        content = message.filename()
        if message.text:
            content = message.text
        payload = {"head": f"A new message from {room.title()}", "body": content, "icon": "/static/chat/img/favicon.png", "url": f"https://orgachat.pythonanywhere.com/chat/room/{room.id}/"}
        for chatter in room.chatters.all():
            if not chatter in message.area.muted_users.all() and chatter != request.user and (True): #todo check for chatter url
                send_user_notification(user=chatter, payload=payload, ttl=1000)

        return redirect('chat:room', room_id=room_id)


@login_required
def save_file_message(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    area = get_object_or_404(Area, pk=int(request.POST.get('area')))
    
    if request.FILES.get("video"):
        message = Message.objects.create(user=request.user, video=request.FILES.get(
            'video'), room=room, area=area)
        message.save()
    elif request.FILES.get("image"):
        message = Message.objects.create(user=request.user, image=request.FILES.get(
            'image'), room=room, area=area)
        message.save()
    elif request.FILES.get("file"):
        message = Message.objects.create(user=request.user, file=request.FILES.get(
            'file'), room=room, area=area)
        message.save()
    elif request.FILES.get("audio"):
        message = Message.objects.create(user=request.user, audio=request.FILES.get(
            'audio'), room=room, area=area)
        message.save()
    return redirect("chat:room", room_id=room.id)


@login_required
def record_audio_message(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    area = get_object_or_404(Area, pk=int(request.POST.get("area")))
    message = Message.objects.create(user=request.user, audio=request.FILES.get("audio"), room=room, area=area)
    message.save()
    return redirect("chat:room", room_id=room.id)



@login_required
def load_messages(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if not request.user in room.chatters.all():
        raise PermissionDenied
    data = json.loads(request.body)
    new_messages = room.message_set.filter(
        ~Q(user=request.user), Q(id__gt=data.get('last_id')))
    json_new_messages = []

    for message in new_messages:
        isText = False
        if message.text:
            isText = True
        json_new_messages.append({
            'user': message.user.username,
            'area': message.area.title,
            'id': message.id,
            'content': message.content(),
            "isText" : isText,
        })
    return JsonResponse({'new_messages': json_new_messages})


# --------Group------------
def create_group(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login to continue")
        return redirect("signupuser")
    room = Room.objects.create(name=request.POST.get('name'), type='group')
    room.save()
    room.chatters.add(request.user)
    area = Area.objects.create(title='Unorganized', room=room)
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
    message = Message.objects.create(
        room=room, text=f"{request.user.username} removed {user.username}", user=request.user)
    message.save()
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
    homepage_area = HomepageArea.objects.create(title=request.POST.get('title'), user=request.user)
    homepage_area.save()
    return redirect('home')

def move_room(request, homepage_area_id):
    try:
        homepage_area = get_object_or_404(HomepageArea, pk=homepage_area_id)
    except:
        homepage_area = None
    room_id = int(json.loads(request.body).get("room_id"))
    room = get_object_or_404(Room, pk=room_id)
    room.homepage_area = homepage_area
    print(room.homepage_area)
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
