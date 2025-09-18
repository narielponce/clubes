from django.urls import path
from .views import (
    ClubHomeView,
    CustomLogoutView,
    DashboardView, 
    GenerateFeesView,
    MemberListView,
    MemberCreateView,
    MemberUpdateView,
    MemberDeleteView
)

urlpatterns = [
    path('', ClubHomeView.as_view(), name='club_home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', CustomLogoutView.as_view(), name='club_logout'),
    path('generar-cuotas/', GenerateFeesView.as_view(), name='generate_fees'),

    # URLs para la gestión de Socios
    path('socios/', MemberListView.as_view(), name='member_list'),
    path('socios/nuevo/', MemberCreateView.as_view(), name='member_create'),
    path('socios/<uuid:pk>/editar/', MemberUpdateView.as_view(), name='member_update'),
    path('socios/<uuid:pk>/eliminar/', MemberDeleteView.as_view(), name='member_delete'),
]
