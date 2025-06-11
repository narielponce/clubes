from django.urls import path
from . import views

app_name = 'disciplinas'

urlpatterns = [
    path('', views.lista_disciplinas, name='lista_disciplinas'),
    # Aquí puedes agregar más rutas según necesites:
    # path('crear/', views.crear_disciplina, name='crear_disciplina'),
    # path('<int:pk>/', views.detalle_disciplina, name='detalle_disciplina'),
    # path('<int:pk>/editar/', views.editar_disciplina, name='editar_disciplina'),
    # path('<int:pk>/eliminar/', views.eliminar_disciplina, name='eliminar_disciplina'),
]
