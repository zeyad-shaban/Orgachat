# Generated by Django 3.1.3 on 2020-12-03 05:09

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_auto_20201203_0504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='video',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True),
        ),
    ]
