from django.shortcuts import get_object_or_404
from .models import Club

class ClubMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extraemos la ruta y la dividimos por '/'
        path_parts = request.path_info.strip('/').split('/')

        # Asumimos que el primer componente de la ruta es el slug del club
        # Ignoramos rutas del admin, accounts, etc.
        if path_parts and path_parts[0] not in ['admin', 'accounts']:
            club_slug = path_parts[0]
            try:
                club = Club.objects.get(subdomain=club_slug, is_active=True)
                request.club = club
            except Club.DoesNotExist:
                request.club = None
        else:
            request.club = None

        response = self.get_response(request)
        return response