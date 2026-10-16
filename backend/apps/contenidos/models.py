from django.db import models


class Nivel(models.TextChoices):
    PRINCIPIANTE = "principiante", "Principiante"
    INTERMEDIO = "intermedio", "Intermedio"
    AVANZADO = "avanzado", "Avanzado"


class Lenguaje(models.Model):
    """Lenguaje de programacion. Solo los 'habilitados' se muestran a los estudiantes."""

    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    descripcion = models.CharField(max_length=200, blank=True)
    habilitado = models.BooleanField(default=False)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Concepto(models.Model):
    """Concepto de programacion (bucles, variables...). Lo usan el PLN, el ML y el recomendador."""

    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    palabras_clave = models.TextField(
        blank=True, help_text="Separadas por coma. Ej: bucle, bucles, for, while, ciclo"
    )

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Tema(models.Model):
    lenguaje = models.ForeignKey(Lenguaje, on_delete=models.CASCADE, related_name="temas")
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    nivel = models.CharField(max_length=20, choices=Nivel.choices, default=Nivel.PRINCIPIANTE)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["lenguaje", "orden"]

    def __str__(self):
        return f"{self.lenguaje} - {self.titulo}"


class Leccion(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name="lecciones")
    titulo = models.CharField(max_length=120)
    contenido = models.TextField(help_text="Explicacion de la leccion")
    ejemplo_codigo = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["tema", "orden"]
        verbose_name = "lección"
        verbose_name_plural = "lecciones"

    def __str__(self):
        return self.titulo


class Ejercicio(models.Model):
    class Tipo(models.TextChoices):
        OPCION_MULTIPLE = "opcion_multiple", "Opción múltiple"
        COMPLETAR_CODIGO = "completar_codigo", "Completar código"
        ESCRIBIR_CODIGO = "escribir_codigo", "Escribir código"

    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name="ejercicios")
    titulo = models.CharField(max_length=120)
    enunciado = models.TextField()
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.ESCRIBIR_CODIGO)
    codigo_inicial = models.TextField(blank=True)
    solucion_referencia = models.TextField(
        blank=True, help_text="Solo para administradores y el tutor. Nunca se envía al estudiante."
    )
    puntos = models.PositiveIntegerField(default=10)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    conceptos = models.ManyToManyField(Concepto, blank=True, related_name="ejercicios")

    class Meta:
        ordering = ["leccion", "orden"]

    def __str__(self):
        return self.titulo


class OpcionEjercicio(models.Model):
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE, related_name="opciones")
    texto = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto


class CasoPrueba(models.Model):
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE, related_name="casos_prueba")
    entrada = models.TextField(blank=True)
    salida_esperada = models.TextField()
    oculto = models.BooleanField(default=False, help_text="Si es oculto, no se muestra la salida esperada")

    def __str__(self):
        return f"Caso de {self.ejercicio}"
