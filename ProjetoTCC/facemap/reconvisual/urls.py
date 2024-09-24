from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('home/', views.home, name='home'),
    path('cadastroalunos/', views.cadastroalunos, name='cadastroalunos'),
    path('facemap/', views.facemap, name='facemap'),
    path('sobre/', views.sobre, name='sobre'),
    path('editarusuario', views.editarusuario, name='editar'),
]