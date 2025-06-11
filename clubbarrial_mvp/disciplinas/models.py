# disciplinas/models.py
from django.db import models
from usuarios.models import CustomUser 
class Disciplina(models.Model):
    nombre = models.CharField(max_length=100)
    coordinador = models.ForeignKey(CustomUser , on_delete=models.CASCADE, related_name='disciplinas')
    def __str__(self):
        return self.nombre
class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='jugadores')
    def __str__(self):
        return self.nombre