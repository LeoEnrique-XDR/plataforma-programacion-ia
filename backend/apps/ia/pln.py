"""PLN: detecta qué conceptos de programación menciona el estudiante en su duda.

Versión inicial: normalización + coincidencia con las palabras clave de cada Concepto.
Siguiente paso: usar spaCy (es_core_news_sm) para lematizar ("bucles" -> "bucle").
"""
import re
import unicodedata


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFD", (texto or "").lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9_]+", " ", texto).strip()


def detectar_conceptos(texto: str, conceptos):
    """Devuelve los conceptos mencionados, del más al menos relevante."""
    t = f" {normalizar(texto)} "
    encontrados = []
    for concepto in conceptos:
        claves = [concepto.nombre] + [k for k in concepto.palabras_clave.split(",") if k.strip()]
        coincidencias = sum(1 for k in claves if f" {normalizar(k)} " in t)
        if coincidencias:
            encontrados.append((coincidencias, concepto))
    encontrados.sort(key=lambda x: -x[0])
    return [c for _, c in encontrados]
