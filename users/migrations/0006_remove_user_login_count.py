# Generated by Django 3.1.2 on 2020-10-20 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_login_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='login_count',
        ),
    ]
