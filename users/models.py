# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass


class Membership(models.Model):
    """
    Representa la membresía de un Usuario a un Club con un rol específico.
    """
    ROLE_ADMIN = 'ADMIN'
    ROLE_TREASURER = 'TREASURER'
    ROLE_INSTRUCTOR = 'INSTRUCTOR'
    ROLE_BOARD = 'BOARD'

    ROLES = (
        (ROLE_ADMIN, 'Administrador'),
        (ROLE_TREASURER, 'Tesorero'),
        (ROLE_INSTRUCTOR, 'Profesor/Instructor'),
        (ROLE_BOARD, 'Comisión Directiva'),
    )

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='memberships')
    club = models.ForeignKey('core.Club', on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLES)

    class Meta:
        verbose_name = "Membresía"
        verbose_name_plural = "Membresías"
        # Asegura que un usuario solo puede tener un rol por club
        unique_together = ('user', 'club')

    def __str__(self):
        return f'{self.user.username} @ {self.club.name} ({self.get_role_display()})'

