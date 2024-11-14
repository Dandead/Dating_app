from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import DatingUser
from profiles.models import DatingProfile


class DatingProfileInline(admin.StackedInline):
    model = DatingProfile
    can_delete = False
    verbose_name_plural = "Profile"


class CustomUserAdmin(UserAdmin):
    inlines = (DatingProfileInline,)
    # model = DatingUser
    list_display = ("email", "is_staff", "is_active", "is_superuser")
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    # "groups", "user_permissions"
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(DatingUser, CustomUserAdmin)
# admin.site.register(DatingProfile)
