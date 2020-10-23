from django.shortcuts import redirect, render

def user_installed(request):
    request.user.is_installed = True
    request.user.save()
    return redirect("home")