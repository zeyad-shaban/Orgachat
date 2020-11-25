# Generated by Django 3.1.3 on 2020-11-25 07:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_last_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_seen',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 11, 25, 7, 31, 31, 147019, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
