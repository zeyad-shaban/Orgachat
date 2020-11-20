from users.models import Category
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
User = get_user_model()


class MyUserAdmin(UserAdmin):
    ordering = ('-date_joined', )
    list_display = ('username', 'email',
                    'date_joined')


MyUserAdmin.list_filter += ('date_joined',)
MyUserAdmin.fieldsets += (('Identifiers', {'fields': (
    'friends', 'avatar', 'about', 'country',)}),)

admin.site.register(User, MyUserAdmin)


@admin.register(Category)
class HomepageAreaAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    list_display = ('title', 'user', 'date')
    readonly_fields = ('date',)
