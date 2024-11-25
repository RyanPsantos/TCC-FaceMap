import cv2
import os
import numpy as np
import json
from django.conf import settings
from pathlib import Path
from reconvisual.models import Aluno  # Importe seu modelo Aluno
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

BASE_DIR = Path(__file__).resolve().parent.parent


# Configuração de classificadores básicos
def configurar_classificadores_basicos():
    """
    Configura apenas os classificadores de rosto e olhos.
    """
    caminho_rosto = str(BASE_DIR / 'static' / 'models' / 'haarcascade_frontalface_default.xml')
    caminho_olho = str(BASE_DIR / 'static' / 'models' / 'haarcascade_eye.xml')

    print(f"Carregando classificadores de: {caminho_rosto} e {caminho_olho}")

    classificador_rosto = cv2.CascadeClassifier(caminho_rosto)
    classificador_olho = cv2.CascadeClassifier(caminho_olho)

    if classificador_rosto.empty() or classificador_olho.empty():
        raise ValueError("Erro ao carregar os classificadores Haar Cascade.")

    return classificador_rosto, classificador_olho


# Configuração do reconhecedor
def configurar_reconhecedor():
    """
    Configura o reconhecedor LBPH e retorna seu caminho.
    """
    reconhecedor = cv2.face.LBPHFaceRecognizer_create(4, 2, 6, 6, 40)
    caminho_modelo = BASE_DIR / 'reconconfig' / 'classificadorLBPHMongo.yml'

    if os.path.exists(caminho_modelo):
        reconhecedor.read(str(caminho_modelo))
        print("Modelo LBPH carregado com sucesso.")
    else:
        print("Modelo LBPH não encontrado. Treinamento necessário.")

    return reconhecedor, caminho_modelo


# Função de captura de imagens
def captura_imagem():
    """
    Captura imagens da câmera e detecta rostos.
    """
    channel_layer = get_channel_layer()  # Inicializar o channel_layer

    # Configurar classificadores e reconhecedor
    classificador_rosto, _ = configurar_classificadores_basicos()
    reconhecedor, caminho_modelo = configurar_reconhecedor()

    if not os.path.exists(caminho_modelo):
        print("O arquivo do classificador não foi encontrado.")
        async_to_sync(channel_layer.group_send)(  # Envia mensagem para o frontend via WebSocket
            "reconhecimento",  
            {
                "type": "send_message",
                "message": "Erro: Classificador não encontrado.",
            },
        )
        return {"status": "erro", "mensagem": "O classificador não foi encontrado"}

    try:
        with open(BASE_DIR / 'reconconfig' / 'id_map.json', 'r') as f:
            id_map = json.load(f)
    except FileNotFoundError:
        async_to_sync(channel_layer.group_send)(
            "reconhecimento",
            {
                "type": "send_message",
                "message": "Erro: Mapeamento de IDs não encontrado. Treine o modelo.",
            },
        )
        return {"status": "erro", "mensagem": "Mapeamento de IDs não encontrado"}

    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not camera.isOpened():
        async_to_sync(channel_layer.group_send)(
            "reconhecimento",
            {
                "type": "send_message",
                "message": "Erro: Não foi possível acessar a câmera.",
            },
        )
        return {"status": "erro", "mensagem": "Erro ao acessar a câmera"}

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Erro ao capturar frame!")
            break

        imagemCinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = classificador_rosto.detectMultiScale(imagemCinza, scaleFactor=1.1, minSize=(30, 30))
        nome = "Não identificado"  # Valor padrão para rostos não identificados

        for (x, y, w, h) in faces:
            rosto = imagemCinza[y:y + h, x:x + w]
            rosto = cv2.resize(rosto, (250, 250))

            try:
                id, confianca = reconhecedor.predict(rosto)

                if confianca < 10:
                    nome = "Nao e um aluno"  # Caso o reconhecimento tenha baixa confiança
                else:
                    aluno_id = id_map.get(str(id))
                    if aluno_id:
                        aluno = Aluno.objects.get(id=aluno_id)
                        nome = aluno.nome_completo
                    else:
                        nome = "Rosto identificado, mas não no mapeamento."

            except Exception as e:
                nome = "Erro no processamento"

            # Enviar a mensagem ao frontend via WebSocket
            async_to_sync(channel_layer.group_send)(
                "reconhecimento",
                {
                    "type": "send_message",
                    "message": nome,
                },
            )

            cv2.putText(frame, nome, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (105, 255, 97), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("Reconhecimento Facial", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    return {"status": "sucesso", "mensagem": "Processo concluído"}



# Treinamento do modelo
def treina_modelo():
    """
    Treina o modelo LBPH com as imagens armazenadas no banco de dados.
    """
    try:
        _, _ = configurar_classificadores_basicos()
        reconhecedor, _ = configurar_reconhecedor()

        alunos = Aluno.objects.all()
        imagens = []
        etiquetas = []
        id_map = {}

        for i, aluno in enumerate(alunos):
            np_array = np.frombuffer(aluno.foto_rosto, dtype=np.uint8)
            imagem = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)

            if imagem is not None:
                imagem = cv2.resize(imagem, (200, 200))
                imagens.append(imagem)
                etiquetas.append(i)
                id_map[str(i)] = str(aluno.id)

        if len(imagens) < 2:
            raise ValueError("Número insuficiente de imagens para treinar o modelo.")

        imagens_np = [np.array(imagem, dtype=np.uint8) for imagem in imagens]
        etiquetas_np = np.array(etiquetas, dtype=np.int32)

        reconhecedor.train(imagens_np, etiquetas_np)
        reconhecedor.write(str(BASE_DIR / 'reconconfig' / 'classificadorLBPHMongo.yml'))

        with open(BASE_DIR / 'reconconfig' / 'id_map.json', 'w') as f:
            json.dump(id_map, f)

        print(f"Mapeamento de IDs salvo: {id_map}")

    except Exception as e:
        print(f"Erro ao treinar modelo: {str(e)}")
        raise


# Consulta de aluno por ID
def analisando_rostos(id):
    """
    Consulta o banco de dados e retorna o nome do aluno pelo ID.
    """
    try:
        aluno = Aluno.objects.get(id=id)
        nome = aluno.nome_completo
        print(f"Aluno identificado: {nome}")
        return nome
    except Aluno.DoesNotExist:
        print(f"ID {id} não encontrado no banco de dados.")
        return "Desconhecido"
