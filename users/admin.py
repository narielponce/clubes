from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Membership


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Configuración del admin para el CustomUser.
    Hereda de UserAdmin para mantener toda la funcionalidad por defecto.
    """
    model = CustomUser


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    """
    Configuración del admin para las Membresías.
    """
    list_display = ('user', 'club', 'role')
    list_filter = ('club', 'role')
    search_fields = ('user__username', 'club__name')
    # autocomplete_fields mejora drásticamente la usabilidad de las ForeignKey
    autocomplete_fields = ('user', 'club')