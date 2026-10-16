from rest_framework import serializers

from .models import CasoPrueba, Ejercicio, Leccion, Lenguaje, OpcionEjercicio, Tema


class LenguajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lenguaje
        fields = ["id", "nombre", "slug", "descripcion"]


class TemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tema
        fields = ["id", "lenguaje", "titulo", "descripcion", "nivel", "orden"]


class LeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leccion
        fields = ["id", "tema", "titulo", "contenido", "ejemplo_codigo", "orden"]


class OpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionEjercicio
        fields = ["id", "texto"]  # nunca se envía 'es_correcta'


class CasoVisibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CasoPrueba
        fields = ["entrada", "salida_esperada"]


class EjercicioSerializer(serializers.ModelSerializer):
    """Nunca expone la solución de referencia ni los casos ocultos."""

    opciones = OpcionSerializer(many=True, read_only=True)
    ejemplos = serializers.SerializerMethodField()

    class Meta:
        model = Ejercicio
        fields = ["id", "leccion", "titulo", "enunciado", "tipo", "codigo_inicial", "puntos", "opciones", "ejemplos"]

    def get_ejemplos(self, obj):
        return CasoVisibleSerializer(obj.casos_prueba.filter(oculto=False), many=True).data
