# Generated by Django 3.1.2 on 2020-10-18 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_auto_20201018_0541'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='content',
            new_name='text',
        ),
    ]
