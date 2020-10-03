from django.contrib import messages
from django.contrib.auth import backends, logout
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, login, authenticate
User = get_user_model()


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
