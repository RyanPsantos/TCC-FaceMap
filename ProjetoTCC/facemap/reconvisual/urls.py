from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teste1/', views.teste1, name='teste1'),
    path('teste2/', views.teste2, name='teste2'),
    path('teste3/', views.teste3, name='teste3'),
]