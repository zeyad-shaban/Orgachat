from django.contrib import admin
from .models import Room, Area, Message


admin.site.register(Room)
admin.site.register(Area)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    '''Admin View for Message'''

    list_display = ('user','room', 'user', 'is_read', 'text')
    readonly_fields = ('date',)