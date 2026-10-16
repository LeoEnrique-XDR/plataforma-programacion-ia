from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.usuarios.urls")),
    path("api/contenidos/", include("apps.contenidos.urls")),
    path("api/progreso/", include("apps.progreso.urls")),
    path("api/tutor/", include("apps.tutor.urls")),
]
