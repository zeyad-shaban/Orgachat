from django.shortcuts import redirect, render

def user_installed(request):
    print("USER INSTALLED THE APP!!!1--------------------------------------")
    print("USER INSTALLED THE APP!!!1--------------------------------------")
    print("USER INSTALLED THE APP!!!1--------------------------------------")
    print("USER INSTALLED THE APP!!!1--------------------------------------")
    request.user.is_installed = True
    request.user.save()
    return redirect("home")