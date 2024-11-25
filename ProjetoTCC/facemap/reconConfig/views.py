from django.http import JsonResponse
from reconvisual.models import Aluno
from .reconhecimento_facial import captura_imagem, treina_modelo, analisando_rostos
from pathlib import Path
import json, os

BASE_DIR = Path(__file__).resolve().parent.parent

def reconhecimento_facial_view(request):
    # Verificar se o classificador já existe
    caminho_modelo = BASE_DIR / 'reconconfig' / 'classificadorLBPHMongo.yml'
    
    if not os.path.exists(caminho_modelo):
        # Se o classificador não existe, treine o modelo
        treina_modelo()
    else:
        # Caso o classificador exista, verificar se há novos registros no banco de dados
        alunos_no_banco = Aluno.objects.all()
        # Obter IDs dos alunos já registrados no classificador
        id_map = {}
        try:
            with open(BASE_DIR / 'reconconfig' / 'id_map.json', 'r') as f:
                id_map = json.load(f)
        except FileNotFoundError:
            pass
        
        alunos_atualizados = [aluno.id for aluno in alunos_no_banco]
        
        if sorted(alunos_atualizados) != sorted(id_map.values()):
            # Se os alunos registrados no banco de dados mudaram, re-treine o modelo
            treina_modelo()

    # Após garantir que o modelo está treinado, capturar a imagem
    resultado = captura_imagem()
    return JsonResponse(resultado)

def treinamento_modelo_view(request):
    treina_modelo()
    return JsonResponse({'status': 'Treinamento do modelo concluído'})

def analisar_rostos_view(request, id):
    nome = analisando_rostos(id)
    return JsonResponse({'nome': nome})

def iniciar_reconhecimento(request):
    resultado = captura_imagem()
    return JsonResponse(resultado)