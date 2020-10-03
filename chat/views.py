from django.contrib import messages
from django.shortcuts import redirect, render

def home(request):
    if request.user.is_authenticated:
        return render(request, 'chat/home.html')
    else:
        messages.error(request, 'Please create an account or login first')
        return redirect('signupuser')