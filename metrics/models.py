from django.db import models


class GrowthReport(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    hypo = models.CharField(max_length=70)
    desc = models.TextField(blank=True, null=True)
    effort_choices = (
        ("easy", "easy < 2 day"),
        ("medium", "medium > 2day > 4 days"),
        ("hard", "hard > 4 days"),
    )
    effort = models.CharField(

        choices=effort_choices, max_length=70)
    # (Users who opened in the last 3 days and joined more than 3 days ago) / (all users ) * 100
    repeat_rate = models.FloatField()
    # (sum of messages in the last 3 days by each user) / (total number of users)
    messages_per_user = models.FloatField()
    # new users in the last 3 days
    new_users_per_day = models.FloatField()
