# usuarios/models.py
from django.contrib.auth.models import AbstractUser 
from django.db import models

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('socio', 'Socio'),
        ('tesorero', 'Tesorero'),
        ('profesor', 'Profesor'),
        ('coordinador', 'Coordinador'),
    ]
    
    # Campos básicos del perfil
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='socio')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    dni = models.CharField(max_length=20, blank=True, null=True, unique=True)
    contacto_emergencia = models.CharField(max_length=100, blank=True, null=True)
    telefono_emergencia = models.CharField(max_length=20, blank=True, null=True)
    
    # Campos de estado
    activo = models.BooleanField(default=True)
    fecha_ingreso = models.DateField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    
    def get_role_display_name(self):
        return dict(self.ROLE_CHOICES).get(self.role, self.role)
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
