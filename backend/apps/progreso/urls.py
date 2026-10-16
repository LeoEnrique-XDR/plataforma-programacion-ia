from django.urls import path

from .views import EnviarRespuestaView, RecomendacionesView, ResumenView, SeleccionarLenguajeView

urlpatterns = [
    path("lenguajes/seleccionar/", SeleccionarLenguajeView.as_view()),
    path("ejercicios/<int:ejercicio_id>/enviar/", EnviarRespuestaView.as_view()),
    path("resumen/", ResumenView.as_view()),
    path("recomendaciones/", RecomendacionesView.as_view()),
]
