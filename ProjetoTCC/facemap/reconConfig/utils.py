import cv2
import numpy as np
import base64
import os 
from pymongo import MongoClient
from datetime import datetime
from PIL import Image
from django.conf import settings

client = MongoClient("mongodb://localhost:27017/")
db = client["db_facemap"]
collection = db["Aluno"]

classificador = cv2.CascadeClassifier(
    os.path.join(settings.STATICFILES_DIRS[0], 'models/haarcascade_frontalface_default.xml')
)
classificadorOlho = cv2.CascadeClassifier(
    os.path.join(settings.STATICFILES_DIRS[0], 'models/haarcascade_eye.xml')
)

reconhecedor = cv2.face.LBPHFaceRecognizer_create()
reconhecedor.read("reconconfig/classificadorLBPHMongo.yml")
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
lbph = cv2.face.LBPHFaceRecognizer_create(2, 4, 8, 8, 50)
camera = cv2.VideoCapture(0)
amostra = 1
numeroAmostras = 25
largura, altura = 220, 220

print("Capturando as faces...")


def captura_imagem():

    while (True):
        conectado, imagem = camera.read()
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


                if cv2.waitKey(1) & 0xFF == ord('q'):
                    imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))

                    _, buffer = cv2.imencode('.jpg', imagemFace)
                    imagemBase64 = base64.b64encode(buffer).decode('utf-8')

                    document = {
                        "imagem": imagemBase64,
                        "data_hora": datetime.now(),
                        "amostra": amostra
                    }
                    collection.insert_one(document)
                    print(f"[foto {amostra} capturada e salva com sucesso no MongoDB]")
                    amostra += 1

        cv2.imshow("Face", imagem)
        cv2.waitKey(1)
        if amostra > numeroAmostras:
            break

    print("Faces capturadas com sucesso")
    camera.release()
    cv2.destroyAllWindows()

    pass

def treina_modelo():

    faces = []
    ids = []

    documentos = collection.find({})

    for documento in documentos:
            imagemNP = np.array(documento['imagem'], dtype = 'uint8')
            id = int(documento['id'])

            ids.append(id)
            faces.append(imagemNP)

            return np.array(ids), faces

    ids, faces = treina_modelo()

    # Treinamento do reconhecedor LBPH
    lbph.train(faces, ids)

    # Salvar o classificador treinado em um arquivo
    lbph.write('reconconfig/classificadorLBPHMongo.yml')

    pass

def analisando_rostos(id):
     
    documento = collection.find_one({"id": id})
    
    if documento:
        return documento['nome'] # Retorna o nome se encontrado
    return "Desconhecido" # Retorna "Desconhecido" se o ID não for encontrado

while True:
    conectado, imagem = camera.read()
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    facesDetectadas = classificador.detectMultiScale(imagemCinza,
                                                    scaleFactor = 1.5,
                                                    minSize=(30, 30))
    for (x, y, l, a) in facesDetectadas:
        imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
        cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255), 2)
        id, confianca = reconhecedor.predict(imagemFace)

        nome = analisando_rostos(id)

        cv2.putText(imagem, nome, (x, y + (a + 30)), font, 2, (0, 0, 255))
        cv2.putText(imagem, str(confianca), (x, y + (a + 50)), font, 1, (0, 0, 255))

    cv2.imshow("Face", imagem)
    if cv2.waitKey(1) == ord('q'):
        break

    camera.release()
    cv2.destroyAllWindows()

    pass