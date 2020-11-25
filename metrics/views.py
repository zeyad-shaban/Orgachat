from datetime import timedelta
from metrics.models import GrowthReport
from django.utils.timezone import now
import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
User = get_user_model()


REPORT_DAYS = 3


@staff_member_required
def index(request):
    return render(request, "metrics/index.html")


# * Should be done once every 3 days
@staff_member_required
def growth_model(request):
    if request.method == 'GET':
        return render(request, "metrics/growth_model.html", {"last_report": GrowthReport.objects.all().last()})
    else:
        hypo = request.POST.get("hypo")
        desc = request.POST.get("desc")
        effort = request.POST.get("effort")

        users = User.objects.all()
        # 1.repeat rate
        repeat_users = User.objects.filter(last_seen__gt=now() - timedelta(days=REPORT_DAYS),
                                           date_joined__lt=now() - timedelta(days=REPORT_DAYS)
                                           )
        repeat_rate = repeat_users.count() / users.count() * 100

        # 2. messages per user
        messages_per_user = sum([user.message_set.filter(
            date__gt=now() - timedelta(days=REPORT_DAYS)).count() for user in users]) / users.count()

        # 3. new users per day
        new_users_per_day = User.objects.filter(
            date_joined__gt=now() - timedelta(days=3)).count() / REPORT_DAYS

        GrowthReport.objects.create(hypo=hypo, desc=desc, effort=effort, repeat_rate=repeat_rate,
                                    messages_per_user=messages_per_user, new_users_per_day=new_users_per_day)
        return redirect("metrics:growth_model")
