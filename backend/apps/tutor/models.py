from django.conf import settings
from django.db import models

from apps.contenidos.models import Ejercicio


class ConsultaTutor(models.Model):
    """Cada consulta al tutor virtual y la pista que devolvió."""

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consultas_tutor")
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.SET_NULL, null=True, blank=True)
    mensaje = models.TextField(blank=True)
    conceptos_detectados = models.JSONField(default=list, blank=True)
    nivel_pista = models.PositiveSmallIntegerField(default=1)
    respuesta = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]
