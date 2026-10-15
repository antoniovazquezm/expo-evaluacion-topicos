from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .api_views import ProyectoViewSet, EvaluadorViewSet, CalificacionViewSet, EstadisticaViewSet

router = DefaultRouter()
router.register(r'proyectos', ProyectoViewSet) #vinvular la ruta proyectos con su clase controlador
router.register(r'evaluadores', EvaluadorViewSet)
router.register(r'calificaciones', CalificacionViewSet)
router.register(r'estadisticas', EstadisticaViewSet, basename="estadisticas")

urlpatterns = [
    path('', include(router.urls)),
]