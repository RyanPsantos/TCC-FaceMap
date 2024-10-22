from django.urls import path
from . import views

urlpatterns = [
    path('camera/', views.ver_camera, name="ver_camera")
]
