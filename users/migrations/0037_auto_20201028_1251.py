# Generated by Django 3.1.2 on 2020-10-28 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_user_login_email_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
