from django.contrib import admin

from .models import CasoPrueba, Concepto, Ejercicio, Leccion, Lenguaje, OpcionEjercicio, Tema


class OpcionInline(admin.TabularInline):
    model = OpcionEjercicio
    extra = 0


class CasoInline(admin.TabularInline):
    model = CasoPrueba
    extra = 0


@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ("titulo", "leccion", "tipo", "puntos", "activo")
    list_filter = ("tipo", "activo", "leccion__tema__lenguaje")
    inlines = [OpcionInline, CasoInline]
    filter_horizontal = ("conceptos",)


@admin.register(Lenguaje)
class LenguajeAdmin(admin.ModelAdmin):
    list_display = ("nombre", "habilitado")
    list_editable = ("habilitado",)
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Concepto)
class ConceptoAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nombre",)}


admin.site.register(Tema)
admin.site.register(Leccion)
