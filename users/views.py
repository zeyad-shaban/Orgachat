from users.forms import UserProfileForm
from django.http import request
from chat.models import Area, Room
from django.contrib import messages
from django.contrib.auth import backends, logout
from django.db.models.query_utils import Q
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, authenticate
User = get_user_model()


def profile(request):
    if request.method == 'GET':
        return render(request, "users/profile.html", {"user_profile_form": UserProfileForm(instance=request.user)})
    else:
        form = UserProfileForm(instance=request.user,
                               data=request.POST, files=request.FILES)
        form.save()
        return redirect("users:profile")


def view_user(request, user_id):
    print(user_id)
    viewed_user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/view_user.html', {'viewed_user': viewed_user})


def all_users(request):
    users = User.objects.filter(~Q(id=request.user.id)).order_by("-last_visit")
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
            messages.warning(request, 'You are already logged in')
            return redirect('home')
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
                messages.success(
                    request, 'Complete your profile so others can find you easily')
                return redirect('users:profile')
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
        messages.success(request, 'Logout out successfullly')
        return redirect('signupuser')

# --------------------
# FAQ and About
# --------------------


def about(request):
    return render(request, "users/about.html")


def search_users(request):
    q = request.GET.get('q')
    users = User.objects.filter(Q(username__icontains=q) | Q(
        email__icontains=q) | Q(country__icontains=q))
    print(users)
    return render(request, "users/all_users.html", {'users': users, 'q': q,})