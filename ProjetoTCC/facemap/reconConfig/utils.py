import cv2
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
    imagens_fotos = []  # Lista para armazenar as imagens capturadas

    while amostra <= numeroAmostras:
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
            
            # Armazenar a imagem capturada na lista
            _, buffer = cv2.imencode('.jpg', imagemFace)
            imagem_binaria = buffer.tobytes()
            imagens_fotos.append(imagem_binaria)

            amostra += 1
            print(f"Foto {amostra - 1} capturada. {numeroAmostras - (amostra - 1)} restantes.")

            # Quando atingir o número de amostras, sai do loop
            if amostra > numeroAmostras:
                break

        # Se você quiser ver a imagem enquanto está detectando
        cv2.imshow("Face", imagem)
        # Se você pressionar 'q', o loop será quebrado.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    camera.release()
    cv2.destroyAllWindows()

    # Retorna todas as imagens capturadas em binário
    return imagens_fotos
