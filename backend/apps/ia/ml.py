"""Machine Learning: detecta los temas donde el estudiante tiene dificultades.

Versión inicial basada en reglas sobre ProgresoConcepto (aciertos/errores).
Cuando el piloto genere datos reales, aquí se entrena un modelo de scikit-learn
(por ejemplo un árbol de decisión) con: aciertos, errores, pistas usadas y tiempo por concepto.
"""
from apps.progreso.models import ProgresoConcepto

MIN_ERRORES = 2
DOMINIO_MINIMO = 0.6


def temas_a_reforzar(usuario, lenguaje, limite=3):
    candidatos = [
        p for p in ProgresoConcepto.objects.filter(usuario=usuario, lenguaje=lenguaje).select_related("concepto")
        if p.errores >= MIN_ERRORES and p.dominio < DOMINIO_MINIMO
    ]
    candidatos.sort(key=lambda p: (p.dominio, -p.errores))
    return candidatos[:limite]
