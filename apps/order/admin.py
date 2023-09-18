from django.contrib import admin

from apps.order import models


class CartItemInlineAdmin(admin.TabularInline):
    model = models.CartItem
    extra = 0
    min_num = 1

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInlineAdmin]

class OrderItemsInlineAdmin(admin.TabularInline):
    model = models.OrderItems
    extra = 0
    min_num = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "user", 
                    "status", "is_viewed", "created_at")
    list_display_links = list_display
    list_filter = ["status"]
    search_fields = ("transaction_id", "status")
    inlines = [OrderItemsInlineAdmin]
    ordering = ["-created_at"]
