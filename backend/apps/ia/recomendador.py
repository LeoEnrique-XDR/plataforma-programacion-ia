"""Sistema de recomendación: elige los siguientes ejercicios según las dificultades."""
from apps.contenidos.models import Ejercicio
from apps.progreso.models import Intento

from .ml import temas_a_reforzar


def recomendar_ejercicios(usuario, lenguaje, n=3):
    """Devuelve una lista de (ejercicio, motivo)."""
    resueltos = Intento.objects.filter(usuario=usuario, correcto=True).values_list("ejercicio_id", flat=True)
    base = Ejercicio.objects.filter(leccion__tema__lenguaje=lenguaje, activo=True).exclude(id__in=resueltos)
    resultado = []

    for p in temas_a_reforzar(usuario, lenguaje):
        for ej in base.filter(conceptos=p.concepto)[:2]:
            resultado.append((ej, f"Refuerzo de {p.concepto.nombre}"))

    if len(resultado) < n:
        ya = {ej.id for ej, _ in resultado}
        siguientes = base.exclude(id__in=ya).order_by("leccion__tema__orden", "leccion__orden", "orden")
        resultado += [(ej, "Siguiente en tu ruta") for ej in siguientes[: n - len(resultado)]]
    return resultado[:n]
