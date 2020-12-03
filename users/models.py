from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import UserManager
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
import humanize
from cloudinary.models import CloudinaryField


class Category(models.Model):
    title = models.CharField(max_length=50)
    is_muted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


class MyUserManager(UserManager):
    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("Admin User must have an email")
        if not password:
            raise ValueError("Admin User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    # * Main
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)
    password = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    # Extra info
    about = models.CharField(
        max_length=190, default="Hi, I use Orgachat!", blank=True, null=True)
    avatar = CloudinaryField('image', default=settings.DEFAULT_USER_AVATAR)

    # Society
    friends = models.ManyToManyField('User', blank=True)
    categories = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True)

    # advance for stuff
    email_code = models.IntegerField(blank=True, null=True)
    expo_push_token = models.TextField(blank=True, null=True)
    last_seen = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()


    def update_last_seen(self):
        self.last_seen = timezone.now()
        return self.save()

    def last_seen_humanize(self):
        timesince = humanize.naturaltime(timezone.now() - self.last_seen)
        if timesince == 'now' or timezone.now() - self.last_seen < timedelta(minutes=2):
            return 'Online'
        return timesince

    def to_json(self):
        try:
            categories = self.categories.all()
        except:
            categories = []
        return {
            "id": self.id,
            "username": self.username,
            "about": self.about,
            "avatar": self.avatar.url,
            "categories": categories,
            'last_seen': self.last_seen_humanize(),
        }

    def __str__(self):
        return str(self.username)
