"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    # order users by id
    ordering = ['id']

    # display email and name columns
    list_display = ['email', 'name']

    # fieldsets used to customize the specific user page
    # need to add customization if using custom user model
    fieldsets = (
        #
        (
            None,
            {
                'fields': (
                    'email',
                    'password',
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                )
            }
        ),
    )

    # set fields to have readonly permission
    readonly_fields = ['last_login']

    # for creating new user in admin panel
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
    )


# display the users using the customized UserAdmin class
admin.site.register(models.User, UserAdmin)
