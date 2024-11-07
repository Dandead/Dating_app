from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import DatingUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    # inlines = [MatchInlineIsLiked, MatchInlineLikes]
    form = CustomUserChangeForm
    model = DatingUser
    list_display = (
        "email",
        "gender",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "gender", "birthday", "avatar")},
        ),
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
                    "avatar",
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
