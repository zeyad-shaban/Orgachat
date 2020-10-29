from django.db import models


class GrowthReport(models.Model):
    hypo = models.CharField(max_length=70)
    desc = models.TextField(blank=True, null=True)
    effort_choices = (
        ("easy", "easy < 2 day"),
        ("medium", "medium > 2day > 4 days"),
        ("hard", "hard > 4 days"),
    )
    effort = models.CharField(
        choices=effort_choices, max_length=70)
    messages_per_day = models.FloatField()
    repeat_rate = models.FloatField()
    new_users_per_day = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
