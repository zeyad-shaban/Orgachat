from metrics.models import GrowthReport
from django.utils.timezone import now
import datetime
from django.db.models.query_utils import Q
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from chat.models import Message
from django.contrib.admin.views.decorators import staff_member_required
User = get_user_model()


@staff_member_required
def index(request):
    return render(request, "metrics/index.html")


@staff_member_required
def growth_model(request):
    if request.method == 'GET':
        return render(request, "metrics/growth_model.html", {"last_report": GrowthReport.objects.all().last()})
    else:
        hypo = request.POST.get("hypo")
        desc = request.POST.get("desc")
        effort = request.POST.get("effort")
        three_days = now() - datetime.timedelta(days=3)
        messages_per_day = (Message.objects.filter(~Q(user=User.objects.get(id=1)), ~Q(
            user=User.objects.get(id=2)), ~Q(user=User.objects.get(id=3)),
            Q(date__gte=three_days)).count()) / 3
        # todo not accurate
        new_users_per_day = User.objects.filter(date_joined__gte=three_days).count()
        growth_report = GrowthReport.objects.create(
            hypo=hypo, desc=desc, effort=effort, messages_per_day=messages_per_day, repeat_rate=repeat_rate, new_users_per_day=new_users_per_day)
        growth_report.save()
        return redirect("metrics:growth_model")
