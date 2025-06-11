from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'activo', 'fecha_ingreso')
    list_filter = ('role', 'activo', 'fecha_ingreso')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': (
            'first_name', 'last_name', 'email', 'dni', 'telefono', 
            'direccion', 'fecha_nacimiento'
        )}),
        ('Contacto de Emergencia', {'fields': (
            'contacto_emergencia', 'telefono_emergencia'
        )}),
        ('Estado y Rol', {'fields': (
            'role', 'activo', 'fecha_ingreso'
        )}),
        ('Permisos', {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'email', 
                'first_name', 'last_name', 'role', 'activo'
            ),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email', 'dni')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(CustomUser, CustomUserAdmin)
