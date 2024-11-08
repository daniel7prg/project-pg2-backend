from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'secciones', SeccionesViewSet, basename='secciones')
router.register(r'unidades', UnidadesViewSet, basename='unidades')
router.register(r'grados', GradosViewSet, basename='grados')
router.register(r'cursos', CursosViewSet, basename='cursos')
router.register(r'alumnos', AlumnosViewSet, basename='alumnos')
router.register(r'notas', NotasViewSet, basename='notas')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = router.urls