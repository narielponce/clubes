from django.db import models
from django.conf import settings
import uuid

class Club(models.Model):
    """
    Representa un Club o Tenant en el sistema SaaS.
    Cada Club es un cliente aislado con sus propios socios, actividades, etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Nombre del Club")
    subdomain = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Subdominio",
        help_text="Subdominio único para el club (ej: 'mi-club')."
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Club"
        verbose_name_plural = "Clubes"
        ordering = ['name']

    def __str__(self):
        return self.name


class Member(models.Model):
    """
    Representa a un socio de un Club.
    """
    STATUS_ACTIVE = 'ACTIVE'
    STATUS_INACTIVE = 'INACTIVE'
    STATUS_SUSPENDED = 'SUSPENDED'

    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Activo'),
        (STATUS_INACTIVE, 'Inactivo'),
        (STATUS_SUSPENDED, 'Suspendido'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='members', verbose_name="Club")
    member_number = models.IntegerField(verbose_name="Número de Socio", editable=False, blank=True)

    first_name = models.CharField(max_length=100, verbose_name="Nombres")
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    email = models.EmailField(max_length=255, blank=True, verbose_name="Email")
    phone_number = models.CharField(max_length=50, blank=True, verbose_name="Teléfono")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    join_date = models.DateField(verbose_name="Fecha de Ingreso")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE, verbose_name="Estado")

    # Vínculo opcional a una cuenta de usuario del sistema
    user_account = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='member_profile',
        verbose_name="Cuenta de Usuario"
    )

    class Meta:
        verbose_name = "Socio"
        verbose_name_plural = "Socios"
        ordering = ['last_name', 'first_name']
        # Un socio tiene un número único dentro de su club
        unique_together = ('club', 'member_number')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name


class Fee(models.Model):
    """
    Representa un cargo financiero (cuota) para un socio.
    """
    STATUS_PENDING = 'PENDING'
    STATUS_PAID = 'PAID'
    STATUS_CANCELED = 'CANCELED'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_PAID, 'Pagada'),
        (STATUS_CANCELED, 'Anulada'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='fees', verbose_name="Socio")
    description = models.CharField(max_length=255, verbose_name="Descripción")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    due_date = models.DateField(verbose_name="Fecha de Vencimiento")
    period = models.DateField(verbose_name="Período al que corresponde")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name="Estado")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cuota"
        verbose_name_plural = "Cuotas"
        ordering = ['-due_date']

    def __str__(self):
        return f'{self.description} - {self.member.full_name} ({self.period.strftime("%Y-%m")})'


class Payment(models.Model):
    """
    Registra un pago realizado por un socio para una cuota específica.
    """
    METHOD_CASH = 'CASH'
    METHOD_TRANSFER = 'TRANSFER'
    METHOD_OTHER = 'OTHER'

    METHOD_CHOICES = (
        (METHOD_CASH, 'Efectivo'),
        (METHOD_TRANSFER, 'Transferencia'),
        (METHOD_OTHER, 'Otro'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name='payments', verbose_name="Cuota")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")
    payment_date = models.DateField(verbose_name="Fecha de Pago")
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default=METHOD_CASH, verbose_name="Método")
    notes = models.TextField(blank=True, verbose_name="Notas")
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='recorded_payments', verbose_name="Registrado por")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-payment_date']

    def __str__(self):
        return f'Pago de {self.amount_paid} para {self.fee.description} de {self.fee.member.full_name}'

    def save(self, *args, **kwargs):
        # Llama al método save original
        super().save(*args, **kwargs)
        # Actualiza el estado de la cuota asociada
        if self.fee.amount <= self.amount_paid:
            self.fee.status = Fee.STATUS_PAID
            self.fee.save()
