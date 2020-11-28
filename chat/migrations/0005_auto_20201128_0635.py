# Generated by Django 3.1.3 on 2020-11-28 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20201124_1006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='file',
        ),
        migrations.AddField(
            model_name='message',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='documents'),
        ),
    ]
