from django.contrib import admin

from .models import Intento, Logro, LogroUsuario, PerfilLenguaje, ProgresoConcepto, Recomendacion

admin.site.register([PerfilLenguaje, ProgresoConcepto, Logro, LogroUsuario, Recomendacion])


@admin.register(Intento)
class IntentoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "ejercicio", "correcto", "pistas_usadas", "creado")
    list_filter = ("correcto",)
