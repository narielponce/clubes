from django.urls import path
from .views import (
    ClubHomeView,
    CustomLogoutView,
    DashboardView, 
    GenerateFeesView,
    MemberListView,
    MemberCreateView,
    MemberUpdateView,
    MemberDeleteView,
    ActivityListView,
    ActivityCreateView,
    ActivityUpdateView,
    ActivityDeleteView
)

urlpatterns = [
    path('', ClubHomeView.as_view(), name='club_home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', CustomLogoutView.as_view(), name='club_logout'),
    path('generar-cuotas/', GenerateFeesView.as_view(), name='generate_fees'),

    # URLs para la gestión de Actividades
    path('actividades/', ActivityListView.as_view(), name='activity_list'),
    path('actividades/nueva/', ActivityCreateView.as_view(), name='activity_create'),
    path('actividades/<uuid:pk>/editar/', ActivityUpdateView.as_view(), name='activity_update'),
    path('actividades/<uuid:pk>/eliminar/', ActivityDeleteView.as_view(), name='activity_delete'),

    # URLs para la gestión de Socios
    path('socios/', MemberListView.as_view(), name='member_list'),
    path('socios/nuevo/', MemberCreateView.as_view(), name='member_create'),
    path('socios/<uuid:pk>/editar/', MemberUpdateView.as_view(), name='member_update'),
    path('socios/<uuid:pk>/eliminar/', MemberDeleteView.as_view(), name='member_delete'),
]
