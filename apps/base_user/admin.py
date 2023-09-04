from django.contrib import admin
from apps.base_user.forms import MyUserChangeForm, MyUserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()

@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'showed_password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'type', 'phone'
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ("email", "first_name", "last_name", 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'showed_password', 'last_login_time')
    list_display_links = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'showed_password')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('type',)

    add_form = MyUserCreationForm
    form = MyUserChangeForm

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during foo creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)