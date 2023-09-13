from django.contrib import admin
from django.utils.safestring import mark_safe

from django.utils.translation import gettext_lazy as _
from apps.product import models


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(models.BrandGroup)
class BrandGroupAdmin(admin.ModelAdmin):
    search_fields = ['name']
    
admin.site.register(models.Discount)
admin.site.register(models.DiscountInfo)

class ProductImageInlineAdmin(admin.TabularInline):
    model = models.ProductImage
    extra = 0
    min = 1

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInlineAdmin]
    empty_value_display = _('-boşdur-')
    list_display = ("code", "name", "price", "stock_count")
    search_fields = ("code", "name", "brand__name", "brand__brand_code")
    autocomplete_fields = ('brand', 'group',)
    list_filter = ("brand__name", "group__name", "stock_status", "updated_at")
    readonly_fields = ('slug', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        (
            _("Önəmli məlumatlar"), {
                "fields": (
                    ('slug', 'code', 'name')
                ),
            }
        ),
        (
            _("Marka məlumatları"), {
                "fields": (
                    ('brand', 'group',)
                ),
            }
        ),
        (
            _("Qiymət məlumatları"), {
                "fields": (
                    ('price', 'discount',)
                ),
            }
        ),
        (
            _("Stok məlumatları"), {
                "fields": (
                    ('stock_status', 'stock_count',)
                ),
            }
        ),
        (
            _("Tarix məlumatları"), {
                "fields": (
                    ('created_at', 'updated_at',)
                ),
            }
        ),
    )

    list_display_links = list_display

@admin.register(models.Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "price", "company")
    list_display_links = list_display
    ordering = ["-created_at"]

@admin.register(models.PopUpSlider)
class PopUpSliderAdmin(admin.ModelAdmin):
    list_display = ("get_image", "title", "is_active", "brand", "group")
    list_display_links = list_display
    ordering = ["-created_at"]

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="40" height="40"')

    get_image.short_description = "Şəkil"
