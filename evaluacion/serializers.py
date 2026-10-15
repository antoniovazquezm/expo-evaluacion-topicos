from rest_framework import serializers
from .models import Proyecto, Evaluador, Calificacion

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ["id", "titulo", "equipo", "categoria"]

class EvaluadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluador
        fields = ["id", "nombre", "email"]

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ["id", "proyecto", "evaluador", "puntaje", "comentario", "fecha"]
