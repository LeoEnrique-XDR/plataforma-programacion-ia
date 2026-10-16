from rest_framework import serializers

from apps.contenidos.models import Nivel


class SeleccionarLenguajeSerializer(serializers.Serializer):
    lenguaje = serializers.SlugField()
    nivel = serializers.ChoiceField(choices=Nivel.choices, default=Nivel.PRINCIPIANTE)


class EnviarRespuestaSerializer(serializers.Serializer):
    respuesta = serializers.CharField(allow_blank=True)
    pistas_usadas = serializers.IntegerField(min_value=0, default=0)
    segundos = serializers.IntegerField(min_value=0, required=False)
