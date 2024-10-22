from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('home/', views.home, name='home'),
    path('cadastroalunos/', views.cadastroalunos, name='cadastroalunos'),
    path('facemap/', views.facemap, name='facemap'),
    path('sobre/', views.sobre, name='sobre'),
    path('editar/', views.editar, name='editar'),
    path('logout/', views.logout, name='logout'),  # Usando seu método de logout personalizado
]