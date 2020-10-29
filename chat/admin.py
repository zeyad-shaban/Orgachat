from django.contrib import admin
from django.urls import resolve
from .models import Room, Area, Message


admin.site.register(Room)
admin.site.register(Area)


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
        elif obj.file:
            return obj.file.url
        elif obj.audio:
            return obj.audio.url