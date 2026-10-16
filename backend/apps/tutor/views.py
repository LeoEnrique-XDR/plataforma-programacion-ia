from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.contenidos.models import Concepto, Ejercicio
from apps.ia import pln, tutor_llm
from apps.progreso.models import Intento

from .models import ConsultaTutor


class PistaSerializer(serializers.Serializer):
    ejercicio = serializers.IntegerField()
    mensaje = serializers.CharField(allow_blank=True, required=False, default="")
    codigo = serializers.CharField(allow_blank=True, required=False, default="")


class PistaView(APIView):
    """El backend decide el nivel de pista (1-3) según los errores y consultas previas."""

    def post(self, request):
        s = PistaSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data
        ejercicio = get_object_or_404(Ejercicio, pk=d["ejercicio"], activo=True)

        errores = Intento.objects.filter(usuario=request.user, ejercicio=ejercicio, correcto=False).count()
        previas = ConsultaTutor.objects.filter(usuario=request.user, ejercicio=ejercicio).count()
        nivel = min(3, max(errores, previas + 1, 1))

        conceptos = pln.detectar_conceptos(d["mensaje"], Concepto.objects.all())
        if not conceptos:
            conceptos = list(ejercicio.conceptos.all())
        respuesta = tutor_llm.generar_pista(ejercicio, d["codigo"], d["mensaje"], nivel, conceptos)

        ConsultaTutor.objects.create(
            usuario=request.user, ejercicio=ejercicio, mensaje=d["mensaje"], nivel_pista=nivel,
            conceptos_detectados=[c.nombre for c in conceptos], respuesta=respuesta,
        )
        return Response({"respuesta": respuesta, "nivel_pista": nivel,
                         "conceptos": [c.nombre for c in conceptos]})
