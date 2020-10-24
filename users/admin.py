from users.models import HomepageArea
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
User = get_user_model()

admin.site.register(User, UserAdmin)


@admin.register(HomepageArea)
class HomepageAreaAdmin(admin.ModelAdmin):
    '''Admin View for HomepageArea'''

    list_display = ('title', 'user', 'date')
    readonly_fields = ('date',)
