import os
from django.contrib.auth import get_user_model
from django.core.checks import messages
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
            if self.type== 'group':
                return f'{messages.last().user.username}: {messages.last().__str__()}'
            return messages.last().__str__()
        return None

    def get_unread_count(self):
        user = current_request().user
        messages = self.message_set.filter(~Q(read_users=user))
        if self.type == 'friend':
            messages = [message for message in messages]
        else:
            messages = [
                message for message in messages if not user in message.channel.muted_users.all()]
        return len(messages)

    def to_json(self, channel=None):
        return {
            "id": self.id,
            "title": self.get_title(),
            "type": self.type,
            "lastMessage": self.last_message(),
            "imageUri": self.get_imageUri(),

            "chatters": [chatter.to_json() for chatter in self.chatters.all()],
            "messages":  [message.to_json() for message in self.message_set.filter(channel=channel).reverse()],
            "channels": [channel.to_json() for channel in self.channel_set.all()],

            "isArchived": self.is_archived,
            "isDeleted": self.is_deleted,
        }

    def to_json_preview(self):
        return {
            "id": self.id,
            "title": self.get_title(),
            "type": self.type,
            "lastMessage": self.last_message(),
            "unreadCount": self.get_unread_count(),
            "imageUri": self.get_imageUri(),
            "isArchived": self.is_archived,
            "isDeleted": self.is_deleted,
        }

    def __str__(self):
        return self.title


class Channel(models.Model):
    title = models.CharField(max_length=30)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    muted_users = models.ManyToManyField(User, blank=True)

    def is_muted(self):
        return current_request().user in self.muted_users.all()

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'chat': {
                'id': self.chat.id
            },
            'is_muted': self.is_muted(),
        }

    def __str__(self):
        return self.title


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    channel = models.ForeignKey(
        Channel, on_delete=models.SET_NULL, blank=True, null=True)

    text = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to="chat/vid", blank=True, null=True)
    image = models.FileField(upload_to="chat/img", blank=True, null=True)
    file = models.FileField(upload_to="chat/file", blank=True, null=True)
    audio = models.FileField(upload_to="chat/aud", blank=True, null=True)

    is_read = models.BooleanField(default=False)
    read_users = models.ManyToManyField(User, related_name="read_users")
    is_deleted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)

        # Send notification
        for chatter in self.chat.chatters.filter(~Q(id=self.user.id)):
            if self.channel and not chatter in self.channel.muted_users.all():
                try:
                    from exponent_server_sdk import PushClient, PushMessage
                    response = PushClient().publish(
                        PushMessage(to=chatter.expo_push_token,
                                    body=f'{self.user.username}: {self.__str__()}',
                                    data={'_displayInForegrouond': True,
                                          'chadId': self.chat.id}
                                    )
                    )
                except:
                    pass

        self.read_users.add(self.user)

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
        if self.channel:
            channel = self.channel.title
        else:
            channel = None
        message = {
            'id': self.id,
            'user': self.user.to_json(),
            'channel': channel,
            'content': self.content(),
            "isText": isText,
            "is_read": self.is_read,
            "is_deleted": self.is_deleted,
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
