from django.core.management.base import BaseCommand

from apps.contenidos.models import CasoPrueba, Concepto, Ejercicio, Leccion, Lenguaje, Tema

LENGUAJES = [
    ("Python", "Fundamentos, automatización y desarrollo general", True),
    ("C", "Fundamentos de programación y gestión de memoria", False),
    ("C++", "Programación estructurada y orientada a objetos", False),
    ("Java", "Programación orientada a objetos y aplicaciones", False),
    ("C#", "Aplicaciones y programación orientada a objetos", False),
    ("JavaScript", "Programación web e interactividad", False),
    ("SQL", "Consultas y bases de datos relacionales", False),
]
CONCEPTOS = [
    ("Variables", "variable, variables, asignar, asignacion"),
    ("Tipos de datos", "tipo, tipos, int, str, float, bool, entero, cadena"),
    ("Conversión de tipos", "int(), conversion, convertir, castear, str(), float()"),
    ("Condicionales", "if, else, elif, condicion, condicional"),
    ("Bucles", "bucle, bucles, for, while, ciclo, repetir, range"),
    ("Funciones", "funcion, funciones, def, return, retorno, parametro"),
]


class Command(BaseCommand):
    help = "Carga lenguajes, conceptos y ejercicios de ejemplo para probar la plataforma."

    def handle(self, *args, **opts):
        from django.utils.text import slugify

        for nombre, desc, hab in LENGUAJES:
            Lenguaje.objects.get_or_create(nombre=nombre, defaults={
                "slug": slugify(nombre.replace("+", "mas").replace("#", "sharp")),
                "descripcion": desc, "habilitado": hab})
        conceptos = {}
        for nombre, claves in CONCEPTOS:
            conceptos[nombre], _ = Concepto.objects.get_or_create(
                nombre=nombre, defaults={"slug": slugify(nombre), "palabras_clave": claves})

        py = Lenguaje.objects.get(nombre="Python")
        tema, _ = Tema.objects.get_or_create(lenguaje=py, titulo="Fundamentos", defaults={"orden": 1})
        l1, _ = Leccion.objects.get_or_create(tema=tema, titulo="Entrada, salida y conversión de tipos", defaults={
            "orden": 1, "contenido": "input() siempre devuelve texto. Para operar con números usa int() o float().",
            "ejemplo_codigo": "edad = int(input())\nprint(edad + 1)"})
        l2, _ = Leccion.objects.get_or_create(tema=tema, titulo="Bucles for", defaults={
            "orden": 2, "contenido": "for repite un bloque de código. range(a, b) va de a hasta b-1.",
            "ejemplo_codigo": "for i in range(3):\n    print(i)"})

        e1, nuevo = Ejercicio.objects.get_or_create(leccion=l1, titulo="El doble de un número", defaults={
            "orden": 1, "puntos": 10, "enunciado": "Lee un número entero y muestra su doble.",
            "solucion_referencia": "n = int(input())\nprint(n * 2)"})
        if nuevo:
            e1.conceptos.set([conceptos["Conversión de tipos"], conceptos["Tipos de datos"]])
            CasoPrueba.objects.create(ejercicio=e1, entrada="4", salida_esperada="8")
            CasoPrueba.objects.create(ejercicio=e1, entrada="10", salida_esperada="20", oculto=True)

        e2, nuevo = Ejercicio.objects.get_or_create(leccion=l2, titulo="Del 1 al 5", defaults={
            "orden": 1, "puntos": 10, "enunciado": "Imprime los números del 1 al 5, uno por línea.",
            "solucion_referencia": "for i in range(1, 6):\n    print(i)"})
        if nuevo:
            e2.conceptos.set([conceptos["Bucles"]])
            CasoPrueba.objects.create(ejercicio=e2, entrada="", salida_esperada="1\n2\n3\n4\n5")
        self.stdout.write(self.style.SUCCESS("Datos de demostración cargados."))
