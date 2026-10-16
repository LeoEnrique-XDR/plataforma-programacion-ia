from datetime import timedelta

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.contenidos.models import Ejercicio, Lenguaje
from apps.contenidos.serializers import EjercicioSerializer
from apps.ia import analisis_codigo, ml, recomendador

from .models import Intento, PerfilLenguaje, ProgresoConcepto
from .serializers import EnviarRespuestaSerializer, SeleccionarLenguajeSerializer


def _actualizar_racha(usuario):
    hoy = timezone.localdate()
    if usuario.ultima_actividad == hoy:
        return
    ayer = hoy - timedelta(days=1)
    usuario.racha_actual = usuario.racha_actual + 1 if usuario.ultima_actividad == ayer else 1
    usuario.ultima_actividad = hoy
    usuario.save(update_fields=["racha_actual", "ultima_actividad"])


class SeleccionarLenguajeView(APIView):
    """El estudiante elige un lenguaje y su nivel. Puede repetirlo con otros lenguajes."""

    def post(self, request):
        s = SeleccionarLenguajeSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        lenguaje = get_object_or_404(Lenguaje, slug=s.validated_data["lenguaje"], habilitado=True)
        perfil, creado = PerfilLenguaje.objects.update_or_create(
            usuario=request.user, lenguaje=lenguaje, defaults={"nivel": s.validated_data["nivel"]}
        )
        return Response({"lenguaje": lenguaje.slug, "nivel": perfil.nivel, "xp": perfil.xp},
                        status=status.HTTP_201_CREATED if creado else status.HTTP_200_OK)


class EnviarRespuestaView(APIView):
    def post(self, request, ejercicio_id):
        ejercicio = get_object_or_404(Ejercicio, pk=ejercicio_id, activo=True)
        s = EnviarRespuestaSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        respuesta = s.validated_data["respuesta"]
        lenguaje = ejercicio.leccion.tema.lenguaje

        if ejercicio.tipo == Ejercicio.Tipo.OPCION_MULTIPLE:
            correcto = ejercicio.opciones.filter(pk=respuesta or 0, es_correcta=True).exists()
            resultado = {"correcto": correcto,
                         "mensaje": "¡Correcto!" if correcto else "Esa no es la opción correcta. Inténtalo de nuevo."}
        elif lenguaje.slug == "python":
            resultado = analisis_codigo.evaluar_python(respuesta, list(ejercicio.casos_prueba.all()))
        else:
            return Response({"detail": f"La evaluación automática de {lenguaje.nombre} aún no está disponible."},
                            status=status.HTTP_501_NOT_IMPLEMENTED)

        correcto = resultado["correcto"]
        primera_vez = correcto and not Intento.objects.filter(
            usuario=request.user, ejercicio=ejercicio, correcto=True).exists()

        Intento.objects.create(
            usuario=request.user, ejercicio=ejercicio, respuesta=respuesta, correcto=correcto,
            retroalimentacion=resultado["mensaje"], pistas_usadas=s.validated_data["pistas_usadas"],
            segundos=s.validated_data.get("segundos"),
        )
        for concepto in ejercicio.conceptos.all():
            p, _ = ProgresoConcepto.objects.get_or_create(
                usuario=request.user, lenguaje=lenguaje, concepto=concepto)
            if correcto:
                p.aciertos += 1
            else:
                p.errores += 1
            p.save()

        xp_ganado = 0
        if primera_vez:
            perfil, _ = PerfilLenguaje.objects.get_or_create(usuario=request.user, lenguaje=lenguaje)
            perfil.xp += ejercicio.puntos
            perfil.save(update_fields=["xp"])
            xp_ganado = ejercicio.puntos
        _actualizar_racha(request.user)

        return Response({**resultado, "xp_ganado": xp_ganado})


class ResumenView(APIView):
    """Datos para el panel de progreso y estadísticas."""

    def get(self, request):
        lenguaje = get_object_or_404(Lenguaje, slug=request.query_params.get("lenguaje"))
        perfil = PerfilLenguaje.objects.filter(usuario=request.user, lenguaje=lenguaje).first()
        stats = Intento.objects.filter(usuario=request.user, ejercicio__leccion__tema__lenguaje=lenguaje).aggregate(
            intentos=Count("id"), aciertos=Count("id", filter=Q(correcto=True)))
        resueltos = Intento.objects.filter(
            usuario=request.user, correcto=True, ejercicio__leccion__tema__lenguaje=lenguaje
        ).values("ejercicio").distinct().count()
        precision = round(100 * stats["aciertos"] / stats["intentos"]) if stats["intentos"] else 0
        return Response({
            "lenguaje": lenguaje.slug,
            "nivel": perfil.nivel if perfil else None,
            "xp": perfil.xp if perfil else 0,
            "racha": request.user.racha_actual,
            "ejercicios_resueltos": resueltos,
            "precision": precision,
            "temas_a_reforzar": [
                {"concepto": p.concepto.nombre, "errores": p.errores, "dominio": p.dominio}
                for p in ml.temas_a_reforzar(request.user, lenguaje)
            ],
        })


class RecomendacionesView(APIView):
    def get(self, request):
        lenguaje = get_object_or_404(Lenguaje, slug=request.query_params.get("lenguaje"))
        items = recomendador.recomendar_ejercicios(request.user, lenguaje)
        return Response([{"ejercicio": EjercicioSerializer(ej).data, "motivo": motivo} for ej, motivo in items])
