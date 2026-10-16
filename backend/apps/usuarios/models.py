from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """Estudiante o administrador de la plataforma."""

    class Rol(models.TextChoices):
        ESTUDIANTE = "estudiante", "Estudiante"
        ADMINISTRADOR = "administrador", "Administrador"

    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.ESTUDIANTE)
    racha_actual = models.PositiveIntegerField(default=0)
    ultima_actividad = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.rol = self.Rol.ADMINISTRADOR
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
