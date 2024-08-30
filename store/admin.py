from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'address', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'address', 'role')}),
    )
    list_display = ['username', 'email', 'phone', 'address', 'role']
    search_fields = ('username', 'email', 'phone')

admin.site.register(CustomUser, CustomUserAdmin)
