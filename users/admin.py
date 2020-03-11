from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.
# class CustomUserAdmin(admin.ModelAdmin):
# username, gender, language, currency, superhost tables 생성
# list_display = ("username", "email", "gender", "language", "currency", "superhost")
# list_filter = ("language","currency","superhost")


@admin.register(models.User)  # decorator 방식
class CustomUserAdmin(UserAdmin):

    """ Custom User admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )
