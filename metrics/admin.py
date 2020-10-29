from metrics.models import GrowthReport
from django.contrib import admin


@admin.register(GrowthReport)
class GrowthReportAdmin(admin.ModelAdmin):
    '''Admin View for GrowthReport'''

    list_display = ('hypo', 'messages_per_day', 'repeat_rate',
                    'new_users_per_day', 'date',)
    readonly_fields = ('date',)
    ordering = ('-date',)
