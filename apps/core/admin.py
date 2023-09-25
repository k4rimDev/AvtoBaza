from django.contrib import admin

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

admin.site.register(models.Slider)
admin.site.register(models.CampaignText)
admin.site.register(models.BrandNumber)
admin.site.register(models.MainData)
admin.site.register(models.SuggestionComplaints)
admin.site.register(models.AboutUs)
