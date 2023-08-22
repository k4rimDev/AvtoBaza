from django.contrib import admin

from apps.product import models


admin.site.register(models.Product)
admin.site.register(models.Brand)
admin.site.register(models.BrandGroup)
admin.site.register(models.Discount)
