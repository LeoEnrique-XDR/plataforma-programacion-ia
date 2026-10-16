from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import LogoutView, PerfilView, RegistroView

urlpatterns = [
    path("registro/", RegistroView.as_view()),
    path("login/", obtain_auth_token),
    path("logout/", LogoutView.as_view()),
    path("perfil/", PerfilView.as_view()),
]
