from rest_framework import serializers

from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "username", "email", "rol", "racha_actual"]
        read_only_fields = fields


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Usuario
        fields = ["username", "email", "password"]

    def create(self, datos):
        # El rol siempre es estudiante: los administradores se crean desde el panel de Django.
        return Usuario.objects.create_user(**datos)
