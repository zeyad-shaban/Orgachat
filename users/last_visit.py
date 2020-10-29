from django.http import HttpResponse
from django.utils.timezone import now
from django.contrib.auth import get_user_model
User = get_user_model()


class SetLastVisitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            User.objects.filter(id=request.user.id).update(last_visit=now())
        return self.get_response(request)