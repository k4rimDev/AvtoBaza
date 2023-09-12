from django.contrib import admin

from apps.account import models


admin.site.register(models.UserTracking)
admin.site.register(models.UserBalance)
