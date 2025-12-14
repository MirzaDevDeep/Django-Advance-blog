from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_superuser', 'is_active', 'created_date')
    list_filter = ('email', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        ('Authentication', {
            'fields': (
                'email', 'password'
            ),
        }),
        ('Permissions', {
            'fields': (
                'is_superuser', 'is_staff', 'is_active'
            ),
        }),
        ('Group permissions', {
            'fields': (
                'groups', 'user_permissions'
            ),
        }),
        ('Important date', {
            'fields': (
                'last_login',
            ),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')
        }),
    )

admin.site.register(Profile)