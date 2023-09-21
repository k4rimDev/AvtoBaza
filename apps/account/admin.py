from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.account import models


@admin.register(models.UserTracking)
class UserTrackingAdmin(admin.ModelAdmin):
    empty_value_display = _('-boşdur-')
    list_display = ("user", "description", "created_at")
    list_display_links = list_display
    search_fields = ("description", "user")
    autocomplete_fields = ('user',)
    list_filter = ("user", )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(models.UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    empty_value_display = _('-boşdur-')
    list_display = ("user", "balance", "remain_balance", "transaction_type")
    list_display_links = list_display
    list_filter = ("transaction_type", )
    search_fields = ("user", )
    autocomplete_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(models.Balance)
class BalanceAdmin(admin.ModelAdmin):
    empty_value_display = _('-boşdur-')
    list_display = ("user", "balance")
    list_display_links = list_display
    search_fields = ("user", )
    autocomplete_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
