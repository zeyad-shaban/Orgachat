from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    friends = models.ManyToManyField('User', blank=True)
    is_installed = models.BooleanField(default=False)