# Generated by Django 3.1.2 on 2020-10-24 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20201024_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, default="Hi! I'm an Orgachat user :)", max_length=250, null=True),
        ),
    ]
