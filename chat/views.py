import json
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from chat.models import Area, Message, Room
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
User = get_user_model()


def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            rooms = Room.objects.all()
            return render(request, 'chat/home.html', {'rooms': rooms})
        else:
            messages.error(request, 'Please create an account or login first')
            return redirect('signupuser')


@csrf_exempt
def room(request, room_id, area_id=None):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'GET':
        for message in room.message_set.all():
            message.is_read = True
            message.save()

        room_messages = room.message_set.all()
        if request.GET.get('area_id'):
            area = get_object_or_404(Area, pk=request.GET.get('area_id'))
            room_messages = room.message_set.filter(area=area)
        return render(request, 'chat/room.html', {'room': room, 'room_messages': room_messages, })
    else:
        data = json.loads(request.body)
        area = get_object_or_404(Area, pk=data.get('area'))
        message = Message.objects.create(
            user=request.user, content=data.get('content'), room=room, area=area)
        message.save()
        return redirect('chat:room', room_id=room_id)

# ----------Area------------


def create_area(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
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
