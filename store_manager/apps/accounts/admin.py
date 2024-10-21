from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Ensure you're importing the correct model

class CustomUserAdmin(UserAdmin):
    # Ensure the field names match the model's attributes
    list_display = ('email', 'cpf', 'phone_number', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name', 'cpf', 'phone_number')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'cpf', 'phone_number', 'street', 'home_number', 'city', 'state', 'country')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'full_name', 'cpf', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    ordering = ('email',)

# Register the CustomUser model with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
