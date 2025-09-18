from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Club, Member
from users.models import Membership

class Command(BaseCommand):
    help = 'Verifica si un usuario tiene una membresía para un club específico.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='El username del usuario a verificar')
        parser.add_argument('club_slug', type=str, help='El subdomain (slug) del club a verificar')

    def handle(self, *args, **options):
        username = options['username']
        club_slug = options['club_slug']
        User = get_user_model()

        self.stdout.write(f"--- Iniciando verificación para usuario '{username}' en club '{club_slug}' ---")

        # 1. Verificar si el usuario existe
        try:
            user = User.objects.get(username=username)
            self.stdout.write(self.style.SUCCESS(f"[OK] Usuario '{username}' encontrado."))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"[ERROR] Usuario '{username}' NO encontrado."))
            return

        # 2. Verificar si el club existe
        try:
            club = Club.objects.get(subdomain=club_slug)
            self.stdout.write(self.style.SUCCESS(f"[OK] Club '{club_slug}' encontrado: {club.name}."))
        except Club.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"[ERROR] Club con slug '{club_slug}' NO encontrado."))
            return

        # 3. Verificar la membresía
        self.stdout.write(f"Buscando membresía que conecte al usuario '{user.id}' con el club '{club.id}'...")
        membership_exists = Membership.objects.filter(user=user, club=club).exists()

        if membership_exists:
            membership = Membership.objects.get(user=user, club=club)
            self.stdout.write(self.style.SUCCESS(f"[¡ÉXITO!] Se encontró una membresía. Rol: {membership.get_role_display()}."))
        else:
            self.stdout.write(self.style.ERROR(f"[FALLO] No se encontró ninguna membresía que conecte a este usuario y club."))

        self.stdout.write("--- Fin de la verificación ---")
