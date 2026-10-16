"""Análisis de código: revisa sintaxis y ejecuta los casos de prueba.

ADVERTENCIA: ejecutar código de estudiantes en el mismo servidor NO es seguro.
Esta versión es solo para desarrollo/demostración (usa un proceso aparte con tiempo límite).
Antes de publicar el sistema, ejecuta el código dentro de un contenedor aislado (Docker) o Judge0.
"""
import ast
import subprocess
import sys
import tempfile

TIEMPO_LIMITE = 5  # segundos por caso de prueba


def evaluar_python(codigo: str, casos) -> dict:
    """Devuelve {'correcto': bool, 'mensaje': str, 'pasados': int, 'total': int}."""
    total = len(casos)
    try:
        ast.parse(codigo)
    except SyntaxError as e:
        return {"correcto": False, "pasados": 0, "total": total,
                "mensaje": f"Error de sintaxis en la línea {e.lineno}: {e.msg}"}

    if total == 0:
        return {"correcto": False, "pasados": 0, "total": 0,
                "mensaje": "Este ejercicio aún no tiene casos de prueba."}

    pasados = 0
    primer_fallo = ""
    with tempfile.TemporaryDirectory() as carpeta:
        for caso in casos:
            try:
                r = subprocess.run(
                    [sys.executable, "-I", "-c", codigo],
                    input=caso.entrada, capture_output=True, text=True,
                    timeout=TIEMPO_LIMITE, cwd=carpeta,
                )
            except subprocess.TimeoutExpired:
                primer_fallo = primer_fallo or "Tu programa tardó demasiado (¿hay un bucle infinito?)."
                continue
            if r.returncode != 0:
                ultima = (r.stderr.strip().splitlines() or ["error desconocido"])[-1]
                primer_fallo = primer_fallo or f"Tu programa falló al ejecutarse: {ultima}"
            elif r.stdout.strip() == caso.salida_esperada.strip():
                pasados += 1
            elif not primer_fallo:
                if caso.oculto:
                    primer_fallo = "La salida no coincide con lo esperado en un caso oculto."
                else:
                    primer_fallo = (f"La salida no coincide. Esperado: {caso.salida_esperada.strip()!r} "
                                    f"· Obtenido: {r.stdout.strip()!r}")
    correcto = pasados == total
    return {"correcto": correcto, "pasados": pasados, "total": total,
            "mensaje": "¡Correcto! Pasaste todos los casos de prueba." if correcto else primer_fallo}
