"""Tutor virtual con Claude (API de Anthropic).

El BACKEND decide el nivel de pista; el modelo solo la redacta.
Además se filtra la salida para que nunca se filtre la solución de referencia.
"""
import re

from django.conf import settings

from .prompts import NIVELES_PISTA, SYSTEM_PROMPT

MENSAJE_SEGURO = ("Intenta releer el enunciado y compara lo que hace tu código con lo que se pide. "
                  "¿En qué paso crees que se separa tu resultado del esperado?")


def _normalizar(texto: str) -> str:
    return re.sub(r"\s+", "", texto or "")


def contiene_solucion(respuesta: str, solucion: str) -> bool:
    """True si la respuesta del modelo copia gran parte de la solución de referencia."""
    lineas = [_normalizar(l) for l in (solucion or "").splitlines()]
    lineas = [l for l in lineas if len(l) >= 6]  # ignora líneas triviales como "else:"
    if not lineas:
        return False
    r = _normalizar(respuesta)
    copiadas = sum(1 for l in lineas if l in r)
    return copiadas / len(lineas) >= 0.6


def generar_pista(ejercicio, codigo: str, mensaje: str, nivel: int, conceptos) -> str:
    if not settings.ANTHROPIC_API_KEY:
        return "El tutor virtual aún no está configurado (falta ANTHROPIC_API_KEY en el archivo .env)."

    import anthropic  # se importa aquí para no exigirlo al arrancar el servidor

    nombres = ", ".join(c.nombre for c in conceptos) or "no identificados"
    pedido = (
        f"{NIVELES_PISTA[nivel]}\n\n"
        f"Ejercicio: {ejercicio.titulo}\nEnunciado: {ejercicio.enunciado}\n"
        f"Conceptos detectados en la duda: {nombres}\n"
        f"Código actual del estudiante:\n{codigo or '(aún no escribió código)'}\n"
        f"Duda del estudiante: {mensaje or '(sin mensaje)'}\n\n"
        f"SOLUCIÓN DE REFERENCIA (CONFIDENCIAL, solo para que tu guía sea correcta; no la reveles):\n"
        f"{ejercicio.solucion_referencia or '(no disponible)'}"
    )
    cliente = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    try:
        resp = cliente.messages.create(
            model=settings.CLAUDE_MODEL, max_tokens=400, system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": pedido}],
        )
        texto = resp.content[0].text
    except Exception:
        return "No pude comunicarme con el tutor en este momento. Intenta de nuevo en unos minutos."

    return MENSAJE_SEGURO if contiene_solucion(texto, ejercicio.solucion_referencia) else texto
