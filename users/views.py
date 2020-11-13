import json
from random import randint

from chat.models import Area, Chat
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers import serialize
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from users.forms import UserProfileForm
from users.serializers import UserSerializer

from .serializers import MyTokenObtainPairSerializer, UserSerializer

from django.contrib.auth import get_user_model
User = get_user_model()


# -------------------------
# AUTHENTICATION
# -------------------------


@api_view(('POST',))
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            if 'is not valid' in serializer.errors['phone_number'][0]:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        phone_number = serializer.initial_data['phone_number'].replace(' ', '')
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            user = User.objects.create_user(
                phone_number=phone_number, username=phone_number)
        user.phone_code = randint(99999, 999999)
        user.save()
        TokenObtainPairView()
        return Response(serializer.data, status.HTTP_200_OK)
        # todo send validation code


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# @api_view(['POST',])
# def loginuser(request):
#     if request.method == 'POST':
#         phone_number = request.data.get('phone_number')
#         try:
#             user = User.objects.get(phone_number=phone_number)
#             if int(request.data.get('phone_code')) == user.phone_code and user.phone_code:
#                 # user.phone_code = None
#                 # user.save()
#                 return Response({'phone_number': phone_number}, status.HTTP_200_OK)

#             else:
#                 return Response({'error': "Invalid code"}, status.HTTP_400_BAD_REQUEST)
#         except Exception as error:
#                 return Response({'error': error}, status.HTTP_500_INTERNAL_SERVER_ERROR)




# ----------Validate-------------



# -------------------------
# USERS
# -------------------------


@ login_required
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
@ login_required
def add_friend(request, user_id):
    print("-------------CALLED-------------")
    friend = get_object_or_404(User, pk=user_id)
    request.user.friends.add(friend)
    friend.friends.add(request.user)
    room = Chat.objects.create(name=friend.username, type="friend")
    room.save()
    room.chatters.add(request.user)
    room.chatters.add(friend)
    area = Area.objects.create(title='general', room=room)
    area.save()
    messages.success(
        request, f'{friend.username} is now a friend, start chatting here <a href="/">Here</a>')
    return redirect('users:all_users')


def remove_friend(request, user_id):
    friend = get_object_or_404(User, pk=user_id)
    request.user.friends.remove(friend)
    friend.friends.remove(request.user)
    rooms = Chat.objects.filter(type='friend')
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
