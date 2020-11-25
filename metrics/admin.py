from metrics.models import GrowthReport
from django.contrib import admin


@admin.register(GrowthReport)
class GrowthReportAdmin(admin.ModelAdmin):
    '''Admin View for GrowthReport'''

    list_display = ('hypo','repeat_rate', 'messages_per_user',
                    'new_users_per_day')
    readonly_fields = ('date',)
    ordering = ('-date',)
