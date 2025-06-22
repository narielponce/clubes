from django.shortcuts import render, get_object_or_404, redirect
from .models import Disciplina
from usuarios.models import SocioDisciplina, CustomUser

def lista_disciplinas(request):
    disciplinas = Disciplina.objects.all()
    return render(request, 'disciplinas/lista_disciplinas.html', {
        'disciplinas': disciplinas,
    })

def detalle_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    socios_participantes = SocioDisciplina.objects.filter(disciplina=disciplina)
    return render(request, 'disciplinas/detalle_disciplina.html', {
        'disciplina': disciplina,
        'socios_participantes': socios_participantes,
    })

def asignar_profesor(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    profesores = CustomUser.objects.filter(role='profesor')
    if request.method == 'POST':
        profesor_id = request.POST.get('profesor')
        profesor = get_object_or_404(CustomUser, id=profesor_id, role='profesor')
        disciplina.coordinador = profesor
        disciplina.save()
        return redirect('disciplinas:detalle_disciplina', disciplina_id=disciplina.id)
    return render(request, 'disciplinas/asignar_profesor.html', {
        'disciplina': disciplina,
        'profesores': profesores,
    })

from .models import Jugador
from .forms import DisciplinaForm
from django.urls import reverse

def registrar_jugador(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        contacto = request.POST.get('contacto')
        if nombre and contacto:
            jugador = Jugador.objects.create(nombre=nombre, contacto=contacto, disciplina=disciplina)
            return redirect('disciplinas:detalle_disciplina', disciplina_id=disciplina.id)
    return render(request, 'disciplinas/registrar_jugador.html', {
        'disciplina': disciplina,
    })

def editar_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            return redirect('disciplinas:detalle_disciplina', disciplina_id=disciplina.id)
    else:
        form = DisciplinaForm(instance=disciplina)
    return render(request, 'disciplinas/editar_disciplina.html', {
        'form': form,
        'disciplina': disciplina,
    })

def crear_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            disciplina = form.save()
            return redirect('disciplinas:detalle_disciplina', disciplina_id=disciplina.id)
    else:
        form = DisciplinaForm()
    return render(request, 'disciplinas/crear_disciplina.html', {
        'form': form,
    })
