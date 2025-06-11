# disciplinas/views.py
from django.shortcuts import render
from .models import Disciplina
def lista_disciplinas(request):
    disciplinas = Disciplina.objects.all()
    return render(request, 'disciplinas/lista_disciplinas.html', {'disciplinas': disciplinas})
