from django.conf import settings
from django.db import models

from apps.contenidos.models import Concepto, Ejercicio, Lenguaje, Nivel


class PerfilLenguaje(models.Model):
    """Progreso de un estudiante en UN lenguaje (nivel y XP son por lenguaje, no globales)."""

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfiles")
    lenguaje = models.ForeignKey(Lenguaje, on_delete=models.CASCADE, related_name="perfiles")
    nivel = models.CharField(max_length=20, choices=Nivel.choices, default=Nivel.PRINCIPIANTE)
    xp = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "lenguaje")

    def __str__(self):
        return f"{self.usuario} - {self.lenguaje}"


class Intento(models.Model):
    """Cada vez que el estudiante envía una respuesta. Es la materia prima del ML."""

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="intentos")
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE, related_name="intentos")
    respuesta = models.TextField(help_text="Código enviado o id de la opción elegida")
    correcto = models.BooleanField(default=False)
    retroalimentacion = models.TextField(blank=True)
    pistas_usadas = models.PositiveSmallIntegerField(default=0)
    segundos = models.PositiveIntegerField(null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]


class ProgresoConcepto(models.Model):
    """Aciertos y errores por concepto, usuario y lenguaje (alimenta al ML y al recomendador)."""

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="progreso_conceptos")
    lenguaje = models.ForeignKey(Lenguaje, on_delete=models.CASCADE)
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE)
    aciertos = models.PositiveIntegerField(default=0)
    errores = models.PositiveIntegerField(default=0)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("usuario", "lenguaje", "concepto")

    @property
    def dominio(self):
        total = self.aciertos + self.errores
        return round(self.aciertos / total, 2) if total else 0.0


class Logro(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.CharField(max_length=200)
    icono = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return self.nombre


class LogroUsuario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="logros")
    logro = models.ForeignKey(Logro, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "logro")


class Recomendacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recomendaciones")
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=200)
    vista = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
