from django.contrib import admin

from apps.order import models


class CartItemInlineAdmin(admin.TabularInline):
    model = models.CartItem
    extra = 0
    min_num = 1

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInlineAdmin]
