from chat.models import Area, Room
from django.contrib import messages
from django.contrib.auth import backends, logout
from django.db.models.query_utils import Q
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, authenticate
User = get_user_model()


def all_users(request):
    users = User.objects.filter(~Q(id=request.user.id))
    return render(request, 'users/all_users.html', {'users': users})


@login_required
def add_friend(request, user_id):
    friend = get_object_or_404(User, pk=user_id)
    request.user.friends.add(friend)
    friend.friends.add(request.user)
    room = Room.objects.create(name=friend.username, type="friend")
    room.save()
    room.chatters.add(request.user)
    room.chatters.add(friend)
    area = Area.objects.create(title='Unorganized', room=room)
    area.save()
    messages.success(
        request, f'You are friends now, start chatting with {friend.username} <a href="/">Here</a>')
    return redirect('users:all_users')


def remove_friend(request, user_id):
    friend = get_object_or_404(User, pk=user_id)
    request.user.friends.remove(friend)
    friend.friends.remove(request.user)
    rooms = Room.objects.filter(type='friend')
    for room in rooms:
        if request.user in room.chatters.all() and friend in room.chatters.all():
            room.delete()
    messages.success(
        request, f'You removed {friend.username} from your friend list')
    return redirect('users:all_users')

# ------------------
# AUTHENTICATION
# ------------------


def signupuser(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.warning(request, 'You are logged in')
            return redirect('signupuser')
        else:
            return render(request, 'users/signupuser.html')
    else:
        if not request.POST.get('password1') == request.POST.get('password1'):
            messages.error(request, 'Passowrd didn\'t match, please try again')
            return redirect('signupuser')
        else:
            try:
                user = User.objects.create_user(username=request.POST.get(
                    'username'), password=request.POST.get('password1'))
                if request.POST.get('email'):
                    user.email = request.POST.get('email')

                user.save()
                login(request, user)
                messages.success(request, 'Created successfully')
                return redirect('home')
            except IntegrityError:
                messages.error(
                    request, 'Username already taken, please try again')
                return redirect('home')


def loginuser(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get(
            'username'), password=request.POST.get('password'), backends='django.contrib.auth.backends.ModelBackend')
        if user:
            login(request, user)
            messages.success(request, f'Welcome back {user.username}')
            return redirect('home')
        else:
            messages.error(
                request, 'Password not correct or user doesn\'t exist, please try again')
            return redirect('signupuser')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
