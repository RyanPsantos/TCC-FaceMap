import cv2
import numpy as np
import base64
import os
import django
from pymongo import MongoClient
from datetime import datetime
from django.conf import settings
from reconvisual.models import Aluno  # Importe seu modelo Aluno
from pathlib import Path

# Inicializa o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facemap.settings')
if not settings.configured:
    django.setup()

# Obter o diretório base do seu projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuração inicial para MongoDB e classificadores
def configurar():
    classificador_rosto = cv2.CascadeClassifier(str(BASE_DIR / 'static' / 'models' / 'haarcascade_frontalface_default.xml'))
    classificador_olho = cv2.CascadeClassifier(str(BASE_DIR / 'static' / 'models' / 'haarcascade_eye.xml'))
    
    if classificador_rosto.empty() or classificador_olho.empty():
        print("Erro ao carregar classificadores de rosto ou olhos. Verifique o caminho.")
        raise ValueError("Erro ao carregar o classificador de rosto. Verifique o caminho.")
    
    reconhecedor = cv2.face.LBPHFaceRecognizer_create()  # Isso só funcionará se você tiver o opencv-contrib-python instalado
    return classificador_rosto, classificador_olho, reconhecedor

# Função para capturar imagens
def captura_imagem():
    classificador_rosto, classificador_olho, _ = configurar()

    if classificador_rosto is None or classificador_olho is None:
        print("Erro ao configurar classificadores.")
        return

    camera = cv2.VideoCapture(0)
    amostra = 1
    numeroAmostras = 25
    
    while True:
        conectado, imagem = camera.read()
        if not conectado:
            print("Erro ao acessar a câmera!")
            break
        
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        facesDetectadas = classificador_rosto.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(150, 150))
        
        for (x, y, l, a) in facesDetectadas:
            cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255), 2)
            regiao = imagem[y:y + a, x:x + l]
            regiaoCinzaOlho = cv2.cvtColor(regiao, cv2.COLOR_BGR2GRAY)
            olhosDetectados = classificador_olho.detectMultiScale(regiaoCinzaOlho)

            for (ox, oy, ol, oa) in olhosDetectados:
                cv2.rectangle(regiao, (ox, oy), (ox + ol, oy + oa), (0, 255, 0), 2)

            # Converte a imagem para base64 quando pressionar 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (200, 200))

                # Armazena a imagem diretamente no MongoDB
                aluno = Aluno(
                    nome_completo=f"Aluno {amostra}",
                    email_institucional=f"aluno{amostra}@exemplo.com",
                    telefone="00000000000",
                    endereco="Rua Exemplo, 123",
                    rg="123456789",
                    registro_matricula=f"2023-{amostra}",
                    data_nascimento=datetime.now(),
                    curso="Curso Exemplo",
                    foto_rosto=imagemFace.tobytes()  # Armazena a imagem como bytes
                )
                aluno.save()
                print(f"[foto {amostra} capturada e salva com sucesso no MongoDB]")
                amostra += 1

        # Exibe a imagem com o rosto detectado e o quadrado vermelho fixo
        cv2.imshow("Face", imagem)
        if amostra > numeroAmostras:
            break

    print("Faces capturadas com sucesso")
    camera.release()
    cv2.destroyAllWindows()

# Função para treinar o modelo
def treina_modelo():
    try:
        _, _, reconhecedor = configurar()
        if reconhecedor is None:
            raise ValueError("Erro ao configurar o reconhecedor.")

        alunos = Aluno.objects.all()
        imagens = []
        etiquetas = []

        for aluno in alunos:
            np_array = np.frombuffer(aluno.foto_rosto, dtype=np.uint8)
            imagem = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)

            if imagem is not None:
                imagens.append(imagem)
                etiquetas.append(int(str(aluno.id)[-6:], 16))

        if len(imagens) < 2:
            raise ValueError("Número insuficiente de imagens para treinar o modelo.")

        imagens_np = [np.array(imagem, dtype=np.uint8) for imagem in imagens]
        etiquetas_np = np.array(etiquetas, dtype=np.int32)

        reconhecedor.train(imagens_np, etiquetas_np)
        reconhecedor.write(str(BASE_DIR / 'reconconfig' / 'classificadorLBPHMongo.yml'))
        print("Modelo treinado com sucesso!")
    except Exception as e:
        raise ValueError(f"Erro ao treinar modelo: {str(e)}")

def analisando_rostos(id):
    try:
        aluno = Aluno.objects.get(id=id)
        return aluno.nome_completo
    except Aluno.DoesNotExist:
        return "Desconhecido"