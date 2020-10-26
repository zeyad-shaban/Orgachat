import os
from users.models import HomepageArea
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
    homepage_area = models.ManyToManyField(HomepageArea, blank=True)

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

    def unread_count(self):
        unread_messages = self.message_set.filter(is_read=False)
        output = []
        for message in unread_messages:
            if message.area and not current_request().user in message.area.muted_users.all() and message.user != current_request().user:
                output.append(message)
        if len(output) <= 0:
            output = 0
        else:
            output = len(output)
        return output

    def __str__(self):
        return str(self.title())

    def last_message(self):
        last_message = self.message_set.all().last()
        if last_message:
            sender = last_message.user
            if sender == current_request().user:
                sender = 'You'
            try:
                return f'({last_message.area.title}) — {sender}: {last_message}'
            except:
                return ''
        else:
            return ''

    def imageURL(self):
        if self.type == 'friend':
            curr_user = current_request().user
            for chatter in self.chatters.all():
                if chatter == curr_user:
                    pass
                else:
                    return chatter.avatar.url
        elif self.type == 'group':
            return "/media/users/img/avatar/DefUser.png"

    def get_homepage_area(self):
        curr_user = current_request().user
        for area in self.homepage_area.all():
            if area in curr_user.homepagearea_set.all():
                return area

        return False


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

    text = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to="chat/room/vid", blank=True, null=True)
    image = models.FileField(upload_to="chat/room/img", blank=True, null=True)
    file = models.FileField(upload_to="chat/room/file", blank=True, null=True)
    audio = models.FileField(upload_to="chat/room/aud", blank=True, null=True)

    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def content(self):
        if self.text:
            return self.text
        elif self.video:
            return f"""
            <video width="320" height="240" controls>
                        <source src="{self.video.url}" type="video/mp4">
                        <source src="{self.video.url}" type="video/mov">
                        <source src="{self.video.url}" type="video/wmv">
                        <source src="{self.video.url}" type="video/avi">
                        <source src="{self.video.url}" type="video/avchd">
                      Your browser does not support the video tag.
                      </video> 
            """
        elif self.image:
            return f'<img src="{self.image.url}" alt="">'
        elif self.file:
            return f'<p><a href="{self.file.url}" download><i class="fas fa-download"></i> {self.filename()}</a></p>'
        elif self.audio:
            return f"""
            <audio controls>
                        <source src="{self.audio.url}" type="audio/pcm">
                        <source src="{self.audio.url}" type="audio/wav">
                        <source src="{self.audio.url}" type="audio/aiff">
                            <source src="{self.audio.url}" type="audio/mp3">
                                <source src="{self.audio.url}" type="audio/aac">
                                <source src="{self.audio.url}" type="audio/ogg">
                                <source src="{self.audio.url}" type="audio/flac">
                                <source src="{self.audio.url}" type="audio/wma">
                      Your browser does not support the audio element.
                      </audio>
            """
        else:
            return self.text

    def is_muted(self):
        show = True
        if current_request().user in self.message.area.muted_users.all():
            pass
        else:
            show = False
        return show

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

    def __str__(self):
        if self.text:
            if len(self.text) > 50:
                return "..." + self.text[:50] + "..."
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
