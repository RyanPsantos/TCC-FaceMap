import cv2
import base64
import os
from django.conf import settings

def configurar_classificadores():
    # Ajuste para garantir que o caminho do classificador está correto
    caminho_classificador = os.path.join(settings, 'facemap/static/models/haarcascade_frontalface_default.xml')
    print(f"Carregando classificador de rosto de: {caminho_classificador}")  # Imprime o caminho do classificador
    
    # Carregar o classificador Haar para detecção de rosto
    classificador_rosto = cv2.CascadeClassifier(caminho_classificador)
    
    if classificador_rosto.empty():
        print("Erro ao carregar o classificador de rosto.")
        return None
    return classificador_rosto

def captura_imagem():
    # Configurar a câmera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Erro ao acessar a câmera!")
        return None
    
    # Carregar o classificador de rosto
    classificador_rosto = configurar_classificadores()
    if classificador_rosto is None:
        return None

    amostra = 1
    numeroAmostras = 25

    while True:
        conectado, imagem = camera.read()
        if not conectado:
            print("Erro ao acessar a câmera!")
            break
        
        # Converter a imagem para escala de cinza
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        
        # Detectar os rostos
        facesDetectadas = classificador_rosto.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(150, 150))

        for (x, y, l, a) in facesDetectadas:
            cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255), 2)
            
            # Processamento do rosto detectado
            imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (200, 200))
            
            # Convertendo a imagem para base64
            _, buffer = cv2.imencode('.jpg', imagemFace)
            imagem_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Retorna a imagem em base64
            return imagem_base64

        # Se você quiser ver a imagem enquanto está detectando
        cv2.imshow("Face", imagem)
        # Se você pressionar 'q', o loop será quebrado.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    camera.release()
    cv2.destroyAllWindows()
    return None
