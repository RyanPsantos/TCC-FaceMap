from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('home/', views.home, name='home'),
    path('reconhecimento/', views.reconhecimento, name='reconhecimento'),
    path('cadastroalunos/', views.cadastroalunos, name='cadastroalunos'),
    path('captura-rosto/', views.captura_rosto, name='captura_rosto'),
    path('facemap/', views.facemap, name='facemap'),
    path('sobre/', views.sobre, name='sobre'),
    path('editar/', views.editar, name='editar'),  # Exibe a lista ou formulário de busca
    path('editar/<str:aluno_id>/', views.editar_aluno, name='editar_aluno'),  # Edita um aluno específico
    path('buscar_aluno/', views.buscar_aluno, name='buscar_aluno'),
    path('logout/', views.logout, name='logout'),
    path('treinar_modelo/', views.treinar_modelo_view, name='treinar_modelo'),
    path('iniciar_reconhecimento/', views.iniciar_reconhecimento, name='iniciar_reconhecimento'),
]