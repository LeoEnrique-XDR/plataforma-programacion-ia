from rest_framework.routers import DefaultRouter

from .views import EjercicioViewSet, LeccionViewSet, LenguajeViewSet, TemaViewSet

router = DefaultRouter()
router.register("lenguajes", LenguajeViewSet, basename="lenguaje")
router.register("temas", TemaViewSet, basename="tema")
router.register("lecciones", LeccionViewSet, basename="leccion")
router.register("ejercicios", EjercicioViewSet, basename="ejercicio")

urlpatterns = router.urls
