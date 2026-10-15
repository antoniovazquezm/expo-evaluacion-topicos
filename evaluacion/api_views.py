from django.shortcuts import render
from rest_framework import viewsets
from .models import Proyecto, Evaluador, Calificacion
from .serializers import ProyectoSerializer, EvaluadorSerializer, CalificacionSerializer
from rest_framework.response import Response
from django.db.models import Avg, Count

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all().order_by("titulo")
    serializer_class = ProyectoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        titulo = self.request.query_params.get("titulo")
        equipo = self.request.query_params.get ("equipo")
        categoria = self.request.query_params.get("categoria")
        evaluador = self.request.query_params.get("evaluador")

        if titulo:
            self.queryset = self.queryset.filter(titulo__icontains = titulo)
        if equipo:
            queryset = queryset.filter(equipo__icontains=equipo)
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        if evaluador:
            queryset = queryset.filter(evaluadores__id=evaluador)

        return queryset

class EvaluadorViewSet(viewsets.ModelViewSet):
    queryset = Evaluador.objects.all().order_by("nombre")
    serializer_class = EvaluadorSerializer

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all().order_by("-fecha")
    serializer_class = CalificacionSerializer

class EstadisticaViewSet(viewsets.ViewSet):
    def list(self, request):
        total_proyectos = Proyecto.objects.count()
        total_evaluadores = Evaluador.objects.count()
        total_calificaciones = Calificacion.objects.count()
        #promedio
        promedio_general = Calificacion.objects.aggregate(Avg("puntaje"))["puntaje__avg"]
        #promedio por categoria
        proyectos_por_categoria = list(
                Proyecto.objects.values("categoria").annotate(total=Count('id'))
            )
        #proyecto más alto
        top_calif = Calificacion.objects.order_by("-puntaje").first()
        top_proyecto = {
                "titulo": top_calif.proyecto.titulo,
                "puntaje": float(top_calif.puntaje)
            } if top_calif else None

        #evaluador que ha calificado más veces
        top_eval_obj = (
                Evaluador.objects.annotate(total=Count("calificaciones"))
                .order_by("-total")
                .first()
            )
        top_evaluador = {
                "nombre": top_eval_obj.nombre,
                "evaluaciones_realizadas": top_eval_obj.total
            } if top_eval_obj else None
        
        return Response({
            "total_proyectos": total_proyectos,
            "total_evaluadores": total_evaluadores,
            "total_calificaciones": total_calificaciones,
            "promedio_general": round(promedio_general, 2) if promedio_general else 0,
            "proyectos_por_categoria": proyectos_por_categoria,
            "top_proyecto": top_proyecto,
            "top_evaluador": top_evaluador,
        })



