from users.models import HomepageArea
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
User = get_user_model()


class MyUserAdmin(UserAdmin):
    ordering = ('-date_joined', )
    list_display = ('username', 'email', 'last_visit',
                    'date_joined', 'is_installed')

MyUserAdmin.list_filter += ('date_joined',)
MyUserAdmin.fieldsets += (('Identifiers', {'fields': ('friends', 'phone_number', 'avatar', 'about', 'country',)}),)
MyUserAdmin.fieldsets += (('Metrics', {'fields': ('is_installed', 'last_visit')}),)

admin.site.register(User, MyUserAdmin)


@admin.register(HomepageArea)
class HomepageAreaAdmin(admin.ModelAdmin):
    '''Admin View for HomepageArea'''

    list_display = ('title', 'user', 'date')
    readonly_fields = ('date',)
