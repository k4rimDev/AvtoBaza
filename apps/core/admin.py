from django.contrib import admin
from django.utils.html import format_html

from apps.core import models

from django_celery_beat.models import IntervalSchedule, PeriodicTask, ClockedSchedule, CrontabSchedule, \
    SolarSchedule
from django_celery_results.models import TaskResult, GroupResult

from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.admin import ResetPasswordTokenAdmin

admin.site.unregister(IntervalSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(ClockedSchedule)

admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)


admin.site.unregister(ResetPasswordToken)

admin.site.register(models.CampaignText)
admin.site.register(models.BrandNumber)
admin.site.register(models.MainData)
admin.site.register(models.SuggestionComplaints)
admin.site.register(models.AboutUs)

@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("get_image", "title", "brand", "group", "is_active")
    list_display_links = list_display

    def get_image(self, obj):
        return format_html(
            '<img src="{}" width="50" height="50"/>'.format(obj.image.url)
        )
    
    get_image.short_description = 'Şəkil'
    get_image.admin_order_field = 'id'
