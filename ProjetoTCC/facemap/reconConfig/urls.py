from django.urls import path
from . import views

urlpatterns = [
    path('reconhecimento_facial/', views.reconhecimento_facial_view, name='reconhecimento_facial'),
    path('treinamento_modelo/', views.treinamento_modelo_view, name='treinamento_modelo'),
    path('analisar_rostos/<str:id>/', views.analisar_rostos_view, name='analisar_rostos')
]
