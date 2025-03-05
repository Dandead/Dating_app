from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import DatingUser, DatingUserNickname, DatingProfile


class DatingProfileInline(admin.StackedInline):
    model = DatingProfile
    can_delete = False
    verbose_name_plural = "Profile"


class DatingUserNicknameInline(admin.StackedInline):
    model = DatingUserNickname
    can_delete = False
    verbose_name_plural = "Nickname"


class CustomUserAdmin(UserAdmin):
    inlines = (DatingProfileInline, DatingUserNicknameInline)
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


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "birthday", "gender")
    list_filter = (
        "user",
        "birthday",
        "gender",
    )


admin.site.register(DatingUser, CustomUserAdmin)
admin.site.register(DatingProfile, ProfileAdmin)
