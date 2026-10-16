from rest_framework import viewsets

from .models import Ejercicio, Leccion, Lenguaje, Tema
from .serializers import EjercicioSerializer, LeccionSerializer, LenguajeSerializer, TemaSerializer


class LenguajeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LenguajeSerializer
    queryset = Lenguaje.objects.filter(habilitado=True)


class TemaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TemaSerializer

    def get_queryset(self):
        qs = Tema.objects.filter(lenguaje__habilitado=True)
        lenguaje = self.request.query_params.get("lenguaje")
        return qs.filter(lenguaje__slug=lenguaje) if lenguaje else qs


class LeccionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeccionSerializer

    def get_queryset(self):
        qs = Leccion.objects.filter(tema__lenguaje__habilitado=True)
        tema = self.request.query_params.get("tema")
        return qs.filter(tema_id=tema) if tema else qs


class EjercicioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EjercicioSerializer

    def get_queryset(self):
        qs = Ejercicio.objects.filter(activo=True, leccion__tema__lenguaje__habilitado=True)
        leccion = self.request.query_params.get("leccion")
        return qs.filter(leccion_id=leccion) if leccion else qs
