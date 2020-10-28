import json
from random import randint

from chat.models import Area, Room
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers import serialize
from django.db.models.query_utils import Q
from django.db.utils import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import UserProfileForm

User = get_user_model()


# -------------------------
# AUTHENTICATION
# -------------------------

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
                user.save()
                login(request, user)
                messages.success(
                    request, 'Validate an email and phone number for your account <a href="/users/send_validation/">here</a>')
                if next != "None" and next:
                    return redirect(next)
                else:
                    return redirect("users:send_validation")
            except IntegrityError:
                messages.error(
                    request, 'Username already taken, please try again')
                return redirect(f'/signup/?next={next}')


def loginuser(request):
    next = request.GET.get("next")
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('home')
        else:
            return render(request, 'users/loginuser.html', {"next": next})

    else:
        try:
            data = json.loads(request.body)
        except:
            data = None
        if data and data.get("email"):
            try:
                user = User.objects.get(email=data.get("email"))
                if user:
                    user.login_email_code = randint(99999, 999999)
                    user.save()
                    send_mail("Orgachat Login with validation code",
                              f"Your validation code: {user.login_email_code}. Copy and paste it to login to your Orgachat account", "officialorgachat@gmail.com", [data.get("email")])
            except User.DoesNotExist:
                return None
        elif request.method == 'POST' and request.POST.get("validation_code"):
            try:
                user = User.objects.get(email=request.POST.get("email"))
                if int(request.POST.get("validation_code")) == user.login_email_code:
                    user.login_email_code = None
                    user.save()
                    login(request, user)
                    if next != "None" and next:
                        return redirect(next)
                    else:
                        return redirect("home")
                else:
                    messages.error(request, 'Wrong validation code')
                    return redirect(f'/login/?next={next}')
            except User.DoesNotExist:
                messages.error(
                    request, 'The email you entered doesn\'t belong to any user')
                return redirect(f'/login/?next={next}')
            except Exception as err:
                print('Error: ', err)
            except MultipleObjectsReturned:
                messages.error(
                    request, 'There are multiple users with the same email address, make sure you typed it correctly')
                return redirect(f'/login/?next={next}')

        else:
            # Login with username/email
            user = authenticate(username=request.POST.get(
                'username'), password=request.POST.get('password'), backends='django.contrib.auth.backends.ModelBackend')
            if user:
                login(request, user)
                if next != "None" and next:
                    return redirect(next)
                else:
                    return redirect("home")
            else:
                messages.error(
                    request, 'Password didn\'t match or user doesn\'t exist, please try again')
        return redirect(f'/login/?next={next}')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser')

# ----------Validate-------------


@login_required
def send_validation(request):
    if request.method == 'GET':
        return render(request, "users/send_validation.html")
    else:
        data = json.loads(request.body)
        if data.get("type") == "phone":
            pass
        elif data.get("type") == "email":
            request.user.email_code = randint(99999, 999999)
            request.user.temp_email = data.get("email")
            request.user.save()
            send_mail("Orgachat Validation code",
                      f"Orgachat Validation code: {request.user.email_code}", "officialorgachat@gmail.com", [data.get("email")])
    return redirect("users:send_validation")


def check_validation(request):
    if request.POST.get("phone_validation_code"):
        pass
    elif request.POST.get("email_validation_code"):
        if int(request.POST.get("email_validation_code")) == request.user.email_code:
            # Cancel every other user email
            try:
                same_email_users = User.objects.filter(
                    email=request.user.temp_email)
                for user in same_email_users:
                    user.email = None
                    user.save()
            except:
                pass
            request.user.email = request.user.temp_email
            request.user.temp_email = None
            request.user.email_code = None
            request.user.save()
            messages.success(
                request, f"Validated Successfully, your account is now linked to {request.user.email}")
        else:
            messages.error(request, "Code isn't valid")

    return redirect('users:send_validation')
# -------------------------
# END AUTHENTICATION
# -------------------------

# -------------------------
# USERS
# -------------------------


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
# -------------------------
# END USERS
# -------------------------


# -------------------------
# ACTIONS
# -------------------------
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

# -------------------------
# END ACTIONS
# -------------------------

# --------------------
# ABOUT
# --------------------


def about(request):
    return render(request, "users/about.html")
