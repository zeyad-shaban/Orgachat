from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.query_utils import Q
from users.get_request import current_request
User = get_user_model()


class Room(models.Model):
    type_choices = [
        ('friend', 'friend'),
        ('group', 'group')
    ]
    type = models.CharField(
        max_length=9, choices=type_choices, default='friend')
    name = models.CharField(max_length=50)
    chatters = models.ManyToManyField(User)

    def title(self):
        if self.type == 'friend':
            curr_user = current_request().user

            for chatter in self.chatters.all():
                if chatter == curr_user:
                    pass
                else:
                    return chatter
        else:
            return self.name

    def __str__(self):
        return str(self.title())

    def unread_count(self):
        unread_messages = self.message_set.filter(is_read=False)
        output = []
        for message in unread_messages:
            if not current_request().user in message.area.muted_users.all():
                output.append(message)
        if len(output) <= 0:
            output = ''
        else:
            output = len(output)
        return output

    def last_message(self):
        last_message = self.message_set.all().last()
        if last_message:
            sender = last_message.user
            if sender == current_request().user:
                sender = 'You'
            return f'{sender} - {last_message.area.title}: {last_message}'
        else:
            return ''


class Area(models.Model):
    title = models.CharField(max_length=30)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    muted_users = models.ManyToManyField(User, blank=True)
    star_users = models.ManyToManyField(
        User, blank=True, related_name='star_users')

    def __str__(self):
        return self.title


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    area = models.ForeignKey(
        Area, on_delete=models.SET_NULL, blank=True, null=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]

    def is_muted(self):
        show = True
        if current_request().user in self.message.area.muted_users.all():
            pass
        else:
            show = False
        return show
