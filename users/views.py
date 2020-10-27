from chat.models import Area, Room
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers import serialize
from django.db.models.query_utils import Q
from django.db.utils import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import json
from users.forms import UserProfileForm

User = get_user_model()


@login_required
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
    q = request.GET.get("q")
    if q:
        users_list = User.objects.filter(Q(username__icontains=q) | Q(
            email__icontains=q) | Q(country__icontains=q)).order_by("-last_visit")
    else:
        users_list = User.objects.filter(
            ~Q(id=request.user.id)).order_by("-last_visit")
    paginator = Paginator(users_list, 12)
    try:
        page = json.loads(request.body)["page"]
    except:
        page = 1
    try:
        users = paginator.page(page)
    except EmptyPage:
        users = []
    except PageNotAnInteger:
        users = paginator.page(1)
    if request.method == 'GET':
        return render(request, 'users/all_users.html', {'users': users, "users_count": users_list.count()})
    else:
        return JsonResponse({"users": serialize("json", users)})


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
        request, f'{friend.username} is now a friend, start chatting here <a href="/">Here</a>')
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
    next = request.GET.get("next")
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('home')
        else:
            return render(request, 'users/signupuser.html', {"next": next})
    else:
        if not request.POST.get('password1') == request.POST.get('password2'):
            messages.error(
                request, 'Confirm password didn\'t match, please try again')
            print(next)
            return redirect(f'/signup/?next={next}')
        else:
            try:
                user = User.objects.create_user(username=request.POST.get(
                    'username'), password=request.POST.get('password1'))
                if request.POST.get('email'):
                    user.email = request.POST.get('email')

                user.save()
                login(request, user)
                messages.success(
                    request, 'Complete your profile so others can know who you are <a href="/users/profile/">here</a>')
                if next != "None" and next:
                    return redirect(next)
                else:
                    return redirect("home")
            except IntegrityError:
                messages.error(
                    request, 'Username already taken, please try again')
                return redirect(f'/signup/?next={next}')


def loginuser(request):
    next = request.GET.get("next")
    if request.method == 'POST':
        user = authenticate(username=request.POST.get(
            'username'), password=request.POST.get('password'), backends='django.contrib.auth.backends.ModelBackend')
        if user:
            login(request, user)
            if next != "None" and next:
                print("THERE IS A NEXT", next)
                return redirect(next)
            else:
                print("TO THE HOME!", next)
                return redirect("home")
        else:
            messages.error(
                request, 'Password didn\'t match or user doesn\'t exist, please try again')
            return redirect(f'/signup/?next={next}')


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

def notif_sub(request):
    notif_sub = json.loads(request.body).get("notif_sub")
    sub_endpoint = notif_sub.get('endpoint')
    sub_auth = notif_sub.get('keys').get('auth')
    sub_p256dh = notif_sub.get('keys').get('p256dh')
    request.user.sub_endpoint = sub_endpoint
    request.user.sub_auth = sub_auth
    request.user.sub_p256dh = sub_p256dh
    request.user.save()
    return redirect("home")