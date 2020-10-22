from django.shortcuts import render


def termsandconditions(request):
    return render(request, "info/termsandconditions.html")


def privacypolicy(request):
    return render(request, "info/privacypolicy.html")

def cookiepolicy(request):
    return render(request, "info/privacypolicy.html")
