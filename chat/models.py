import os
from django.core.serializers import serialize
from users.models import Category
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.query_utils import Q
from users.get_request import current_request
User = get_user_model()


class Chat(models.Model):
    type_choices = [
        ('friend', 'friend'),
        ('group', 'group')
    ]
    type = models.CharField(
        max_length=9, choices=type_choices, default='friend')
    title = models.CharField(max_length=50)
    image = models.FileField(
        upload_to="chat/room/chat_image", blank=True, null=True, default="users/img/avatar/DefUser.png")
    chatters = models.ManyToManyField(User)
    is_deleted = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def get_title(self):
        if self.type == "friend":
            curr_user = current_request().user
            for chatter in self.chatters.all():
                if not chatter == curr_user:
                    return chatter.username
        else:
            return self.title

    def get_imageUri(self):
        if self.type == "friend":
            curr_user = current_request().user
            for chatter in self.chatters.all():
                if not chatter == curr_user:
                    return chatter.avatar.url
        else:
            return self.image.url

    def last_message(self):
        messages = self.message_set.all()
        if messages.count() > 0:
            return messages.last().__str__()
        return ""

    def to_json(self):
        return {
            "id": self.id,
            "title": self.get_title(),
            "lastMessagge": self.last_message(),
            "messages":  [message.to_json() for message in self.message_set.all().reverse()],
            "imageUri": self.get_imageUri(),
            "type": self.type,
            "chatters": [chatter.to_json() for chatter in self.chatters.all()],
            "isArchived": self.is_archived,
            "isDeleted": self.is_deleted,
        }

    def __str__(self):
        return self.title


class Area(models.Model):
    title = models.CharField(max_length=30)
    room = models.ForeignKey(Chat, on_delete=models.CASCADE)
    muted_users = models.ManyToManyField(User, blank=True)
    star_users = models.ManyToManyField(
        User, blank=True, related_name='star_users')

    def __str__(self):
        return self.title


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    area = models.ForeignKey(
        Area, on_delete=models.SET_NULL, blank=True, null=True)

    text = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to="chat/vid", blank=True, null=True)
    image = models.FileField(upload_to="chat/img", blank=True, null=True)
    file = models.FileField(upload_to="chat/file", blank=True, null=True)
    audio = models.FileField(upload_to="chat/aud", blank=True, null=True)

    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def filename(self):
        if self.video:
            return os.path.basename(self.video.name)
        elif self.image:
            return os.path.basename(self.image.name)
        elif self.file:
            return os.path.basename(self.file.name)
        elif self.audio:
            return os.path.basename(self.audio.name)
        else:
            return self.text

    def content(self):
        if self.text:
            return self.text
        elif self.video:
            return self.video.url
        elif self.image:
            return self.image.url
        elif self.file:
            return self.file.url
        elif self.audio:
            return self.audio.url

    def to_json(self):
        isText = False
        if self.text:
            isText = True
        if self.area:
            area_title = self.area.title
        else:
            area_title = None
        message = {
            'id': self.id,
            'user': self.user.to_json(),
            'area': area_title,
            'content': self.content(),
            "isText": isText,
            # "date": self.date,
            # todo "time_since":
        }
        return message

    def __str__(self):
        if self.text:
            if self.text.replace(" ", "") == "":
                return ""
            return self.text[:30]
        elif self.video:
            return "🎥 Video"
        elif self.image:
            return "📷 Image"
        elif self.file:
            return "🗂 File"
        elif self.audio:
            return "🔊 Audio"
