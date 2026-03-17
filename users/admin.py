from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ("id", "email", "phone_number", "is_active", "is_superuser")
    ordering = ("email",)
    search_fields = ("email", "phone_number")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    filter_horizontal = ("groups", "user_permissions") 
    fieldsets = (
        (None, {"fields": ("email", "phone_number","birthdate",  "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone_number","birthdate", "password1", "password2", "is_staff", "is_superuser", "is_active"),
        }),
    )