from django.urls import path
from . import views

app_name = 'disciplinas'

urlpatterns = [
    path('', views.lista_disciplinas, name='lista_disciplinas'),
    path('crear/', views.crear_disciplina, name='crear_disciplina'),
    path('<int:disciplina_id>/asignar_profesor/', views.asignar_profesor, name='asignar_profesor'),
    path('<int:disciplina_id>/registrar_jugador/', views.registrar_jugador, name='registrar_jugador'),
    path('<int:disciplina_id>/editar/', views.editar_disciplina, name='editar_disciplina'),
    path('<int:disciplina_id>/detalle/', views.detalle_disciplina, name='detalle_disciplina'),
]
