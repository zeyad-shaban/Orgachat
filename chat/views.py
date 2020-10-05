import json
from django.core.exceptions import PermissionDenied
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from chat.models import Area, Message, Room
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
User = get_user_model()


def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            rooms = Room.objects.filter(chatters=request.user)
            return render(request, 'chat/home.html', {'rooms': rooms})
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
            user=request.user, content=data.get('content'), room=room, area=area)
        message.save()
        return redirect('chat:room', room_id=room_id)


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
        json_new_messages.append({
            'user': message.user.username,
            'content': message.content,
            'area': message.area.title,
            'id': message.id
        })
    return JsonResponse({'new_messages': json_new_messages})


# --------Group------------
def create_group(request):
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
        room=room, content=f"{request.user.username} removed {user.username}", user=request.user)
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
