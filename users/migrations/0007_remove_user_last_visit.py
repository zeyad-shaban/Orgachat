# Generated by Django 3.1.2 on 2020-10-20 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_user_login_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_visit',
        ),
    ]
