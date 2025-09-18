from django.contrib import admin
from .models import Club, Member, Fee


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Club.
    """
    list_display = ('name', 'subdomain', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'subdomain')
    ordering = ('name',)
    readonly_fields = ('id', 'created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'subdomain', 'is_active')
        }),
        ('Información del Sistema', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Member.
    """
    list_display = ('full_name', 'club', 'status', 'member_number', 'join_date')
    list_filter = ('club', 'status')
    search_fields = ('first_name', 'last_name', 'member_number', 'email')
    ordering = ('last_name', 'first_name')
    autocomplete_fields = ('club', 'user_account')
    readonly_fields = ('id',)

    fieldsets = (
        ('Información del Club', {
            'fields': ('club', 'member_number', 'status', 'join_date')
        }),
        ('Datos Personales', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'birth_date')
        }),
        ('Sistema', {
            'fields': ('id', 'user_account'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    """
    Configuración del admin para las Cuotas (Fees).
    """
    list_display = ('member', 'description', 'amount', 'due_date', 'status', 'get_club')
    list_filter = ('status', 'member__club')
    search_fields = ('description', 'member__first_name', 'member__last_name')
    ordering = ('-due_date',)
    list_select_related = ('member', 'member__club')  # Optimización de rendimiento
    autocomplete_fields = ('member',)

    @admin.display(description='Club')
    def get_club(self, obj):
        return obj.member.club