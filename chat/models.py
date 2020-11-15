import os
from users.models import Category
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.query_utils import Q
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
        upload_to="chat/room/chat_image", blank=True, null=True)
    chatters = models.ManyToManyField(User)
    is_deleted = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def to_json(self):
        if self.type == "friend":
            title = "OtherFriend Username"
            imageUri = "OtherFriend Image URI"
        else:
            title = "A chat with a group"
            imageUri = self.image

        json_chat = {
            "title": title,
            "imageUri": imageUri,
            "lastMessagge": self.message_set.all().last(),
            "type": self.type,
            "chatters": [chatter.to_json() for chatter in self.chatters.all()],
            "isArchived": self.is_archived,
            "isDeleted": self.is_deleted,
        }

        return json_chat

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
    room = models.ForeignKey(Chat, on_delete=models.CASCADE)
    area = models.ForeignKey(
        Area, on_delete=models.SET_NULL, blank=True, null=True)

    text = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to="chat/room/vid", blank=True, null=True)
    image = models.FileField(upload_to="chat/room/img", blank=True, null=True)
    file = models.FileField(upload_to="chat/room/file", blank=True, null=True)
    audio = models.FileField(upload_to="chat/room/aud", blank=True, null=True)

    is_read = models.BooleanField(default=False)
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

    def json(self):
        isText = False
        if self.text:
            isText = True
        if self.area:
            area_title = self.area.title
        else:
            area_title = None
        message = {
            'user': self.user.username,
            'area': area_title,
            'id': self.id,
            'content': self.content(),
            "isText": isText,
            "date": self.date,
            # todo "time_since":
        }
        return message

    def __str__(self):
        if self.text:
            if len(self.text) > 50:
                return "..." + self.text[:30] + "..."
            else:
                return self.text
        elif self.video:
            return "🎥 Video"
        elif self.image:
            return "📷 Image"
        elif self.file:
            return "🗂 File"
        elif self.audio:
            return "🔊 Audio"
