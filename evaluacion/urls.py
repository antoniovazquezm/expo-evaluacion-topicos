from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ProyectoViewSet, EvaluadorViewSet, CalificacionViewSet

router = DefaultRouter()
router.register(r'proyectos', ProyectoViewSet)
router.register(r'evaluadores', EvaluadorViewSet)
router.register(r'calificaciones', CalificacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]