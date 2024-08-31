from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Tenant, ServiceProvider, DemoRequests


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "username", "username_slug", "role", "phone", "is_active"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            "Personal info",
            {
                "fields": [
                    "username",
                    "username_slug",
                    "profile",
                    "role",
                    "phone",
                    "address",
                ]
            },
        ),
        ("Permissions", {"fields": ["is_admin", "is_active", "is_verified"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "username",
                    "address",
                    "phone",
                    "role",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]
    search_fields = ["email", "username_slug"]
    ordering = ["email", "id"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.register(Tenant)
admin.site.register(ServiceProvider)
admin.site.register(DemoRequests)
