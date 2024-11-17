from django.http import JsonResponse
from .reconhecimento_facial import captura_imagem, treina_modelo, analisando_rostos

def reconhecimento_facial_view(request):
    resultado = captura_imagem()
    return JsonResponse(resultado)

def treinamento_modelo_view(request):
    treina_modelo()
    return JsonResponse({'status': 'Treinamento do modelo concluído'})

def analisar_rostos_view(request, id):
    nome = analisando_rostos(id)
    return JsonResponse({'nome': nome})