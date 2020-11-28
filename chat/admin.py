from django.contrib import admin
from django.urls import resolve
from .models import Chat, Channel, Message


admin.site.register(Chat)
admin.site.register(Channel)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    '''Admin View for Message'''

    list_display = ('user', 'is_read', 'get_content', 'date')
    def get_content(self, obj):
        if obj.text:
            return obj.text
        elif obj.video:
            return obj.video.url
        elif obj.image:
            return obj.image.url
        elif obj.document:
            return obj.document.url
        elif obj.audio:
            return obj.audio.url