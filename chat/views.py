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
def room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'GET':
        for message in room.message_set.all():
            message.is_read = True
            message.save()
        return render(request, 'chat/room.html', {'room': room})
    else:
        data = json.loads(request.body)
        area = get_object_or_404(Area, pk=data.get('area'))
        all_area = Area.objects.filter(
            (Q(title='all') | Q(title='All')), room=room)[0]
        message = Message.objects.create(
            user=request.user, content=data.get('content'), room=room)
        message.save()
        message.area.add(area)
        if all_area and not all_area == area:
            message.area.add(all_area)

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
    print(area.muted_users.all())
    return redirect('chat:room', area.room.id)