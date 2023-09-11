from django.contrib import admin

from apps.product import models


admin.site.register(models.Brand)
admin.site.register(models.BrandGroup)
admin.site.register(models.Discount)

class ProductImageInlineAdmin(admin.TabularInline):
    model = models.ProductImage
    extra = 0
    min = 1

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInlineAdmin]
    list_display = ("code", "name", "price", "stock_count")
    list_display_links = list_display
