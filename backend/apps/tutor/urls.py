from django.urls import path

from .views import PistaView

urlpatterns = [path("pista/", PistaView.as_view())]
