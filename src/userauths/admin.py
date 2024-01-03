from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "username",
        "first_name",
        "email",
        "phone_number",
        "address",
        
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("phone_number","address")}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("phone_number","address")}),)


admin.site.register(CustomUser, CustomUserAdmin)


