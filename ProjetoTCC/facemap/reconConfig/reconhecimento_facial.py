import cv2
import numpy as np
import base64
import os
import django
from pymongo import MongoClient
from datetime import datetime
from django.conf import settings
from reconvisual.models import Aluno  # Importe seu modelo Aluno

# Inicializa o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facemap.settings')
if not settings.configured:
    django.setup()

# Configuração inicial para MongoDB e classificadores
def configurar():
    # Carregar classificadores em cascata
    classificador_rosto = cv2.CascadeClassifier('C:/Users/CAMARGO/Desktop/TCC-FaceMap/ProjetoTCC/facemap/static/models/haarcascade_frontalface_default.xml')
    classificador_olho = cv2.CascadeClassifier('C:/Users/CAMARGO/Desktop/TCC-FaceMap/ProjetoTCC/facemap/static/models/haarcascade_eye.xml')
    
    # Verificar se os classificadores foram carregados corretamente
    if classificador_rosto.empty() or classificador_olho.empty():
        print("Erro ao carregar classificadores de rosto ou olhos. Verifique o caminho.")
        return
    
    # Inicializar o reconhecedor de rostos
    reconhecedor = cv2.face.LBPHFaceRecognizer_create()  # Isso só funcionará se você tiver o opencv-contrib-python instalado
    return reconhecedor

configurar()  # Configuração inicial do MongoDB e classificadores

# Função para capturar imagens
def captura_imagem():
    camera = cv2.VideoCapture(0)
    amostra = 1
    numeroAmostras = 25
    
    while True:
        conectado, imagem = camera.read()
        if not conectado:
            print("Erro ao acessar a câmera!")
            break
        
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        facesDetectadas = classificador.detectMultiScale(imagemCinza,
                                                         scaleFactor=1.5,
                                                         minSize=(150, 150))
        for (x, y, l, a) in facesDetectadas:
            cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255), 2)
            regiao = imagem[y:y + a, x:x + l]
            regiaoCinzaOlho = cv2.cvtColor(regiao, cv2.COLOR_BGR2GRAY)
            olhosDetectados = classificadorOlho.detectMultiScale(regiaoCinzaOlho)

            for (ox, oy, ol, oa) in olhosDetectados:
                cv2.rectangle(regiao, (ox, oy), (ox + ol, oy + oa), (0, 255, 0), 2)

            # Converte a imagem para base64 quando pressionar 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))

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

        # Exibe a imagem com o rosto detectado
        cv2.imshow("Face", imagem)
        if amostra > numeroAmostras:
            break

    print("Faces capturadas com sucesso")
    camera.release()
    cv2.destroyAllWindows()

# Função para treinar o modelo
def treina_modelo():
    faces = []
    ids = []

    documentos = Aluno.objects()  # Mudei para usar o MongoEngine
    for documento in documentos:
        imagem = np.frombuffer(documento.foto_rosto, dtype=np.uint8)  # Carregue a imagem em bytes
        faces.append(cv2.imdecode(imagem, cv2.IMREAD_GRAYSCALE))
        ids.append(str(documento.id))  # Usando id do MongoDB como identificador único

    lbph.train(faces, np.array(ids))
    lbph.write('reconconfig/classificadorLBPHMongo.yml')
    print("Modelo treinado e salvo com sucesso")

# Função para reconhecer rostos detectados
def analisando_rostos(id):
    aluno = Aluno.objects.get(id=id)
    if aluno:
        return aluno.nome_completo
    return "Desconhecido"
