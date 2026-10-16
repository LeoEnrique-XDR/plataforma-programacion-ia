from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Plataforma", {"fields": ("rol", "racha_actual", "ultima_actividad")}),)
    list_display = ("username", "email", "rol", "is_active")
