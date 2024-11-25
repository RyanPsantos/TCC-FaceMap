from .models import Professor, Aluno
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.conf import settings
from mongoengine.errors import DoesNotExist
from django.http import JsonResponse
from reconconfig.utils import captura_imagem, configurar_classificadores  # Certifique-se que esta importação está correta
from reconconfig.reconhecimento_facial import treina_modelo
from reconconfig import reconhecimento_facial
from reconconfig.reconhecimento_facial import captura_imagem
import cv2
import os
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def captura_imagem_e_identificar_com_lbph(request):
    #Captura a imagem da câmera, faz o reconhecimento facial e tenta identificar no banco de dados.
    classificador_rosto = configurar_classificadores()
    if classificador_rosto is None:
        return render(request, 'reconvisual/reconhecimento.html', {"mensagem": "Erro ao configurar o classificador de rosto."})
        
    # Carregar o modelo LBPH treinado
    caminho_modelo = os.path.join(settings.BASE_DIR, 'reconconfig', 'classificadorLBPHMongo.yml')
    reconhecedor = cv2.face.LBPHFaceRecognizer_create(2, 2, 5, 5, 30)
    reconhecedor.read(caminho_modelo)
    if not os.path.exists(caminho_modelo):
        return render(request, 'reconvisual/reconhecimento.html', {"mensagem": "O arquivo do classificador não foi encontrado."})
    else:
        print("Classificador carregado com sucesso.")

    # Configurar a câmera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        return render(request, 'reconvisual/reconhecimento.html', {"mensagem": "Erro ao capturar a imagem da câmera."})
 
    while True:
        conectado, imagem = camera.read()
        if not conectado:
            return render(request, 'reconvisual/reconhecimento.html', {"mensagem": "Erro ao capturar a imagem da câmera."})
        
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        facesDetectadas = classificador_rosto.detectMultiScale(imagemCinza, scaleFactor=1.3, minSize=(100, 100))

        for (x, y, l, a) in facesDetectadas:
            cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 255, 0), 2)
            # Extrair o rosto detectado
            rosto = imagemCinza[y:y + a, x:x + l]
            rosto = cv2.resize(rosto, (200, 200))

            # Reconhecer o rosto usando o LBPH
            id, confianca = reconhecedor.predict(rosto)
            print(f"ID Predito: {id}, Confiança: {confianca}")

            # Definir limite de confiança para reconhecer a pessoa
            if confianca < 50:  # Ajuste o limiar conforme necessário
                try:
                    aluno = Aluno.objects.get(id=id)
                    nome = aluno.nome_completo
                except Aluno.DoesNotExist:
                    nome = "Aluno nao encontrado"
            else:
                nome = "Nao e um aluno"

            fonte = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(imagem, nome, (x, y + a + 20), fonte, 0.8, (0, 255, 0), 2)

        cv2.imshow("Reconhecimento Facial", imagem)

        # Quebrar o loop ao pressionar a tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

    return render(request, 'reconvisual/reconhecimento.html', {"mensagem": nome})

def iniciar_reconhecimento(request):
    try:
        resultado = captura_imagem()
        return JsonResponse(resultado)
    except Exception as e:
        return JsonResponse({"status": "erro", "mensagem": f"Erro: {str(e)}"}, status=500)
    
def treinar_modelo_view(request):
    try:
        treina_modelo()
        return JsonResponse({'success': True, 'message': 'Modelo treinado com sucesso!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro ao treinar modelo: {str(e)}'})

def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        try:
            professor = Professor.objects.get(username=username)
            if check_password(senha, professor.senha):
                request.session['usuario_id'] = professor.id
                request.session['usuario_nome'] = professor.username
                messages.success(request, "Login realizado com sucesso!")
                return redirect('home')
            else:
                messages.error(request, "Nome de usuário ou senha incorretos.")
        except Professor.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
    return render(request, 'reconvisual/index.html')

def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email_institucional = request.POST.get('email_institucional')
        telefone = request.POST.get('telefone')
        senha = request.POST.get('senha')
        conf_senha = request.POST.get('conf_senha')

        if senha != conf_senha:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'reconvisual/cadastro.html')
        
        try:
            novo_professor = Professor(
                username=username,
                email_institucional=email_institucional,
                telefone=telefone,
                senha=make_password(senha),
            )
            novo_professor.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('index')
        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {e}")
    return render(request, 'reconvisual/cadastro.html')

@login_required
def home(request):
    return render(request, 'reconvisual/home.html', {'usuario_nome': request.session.get('usuario_nome', 'Usuário')})

@login_required
def reconhecimento(request):
    return render(request, 'reconvisual/reconhecimento.html')

@login_required
def cadastroalunos(request):
    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        email_institucional = request.POST.get('email_institucional')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        rg = request.POST.get('rg')
        registro_matricula = request.POST.get('registro_matricula')
        data_nascimento = request.POST.get('data_nascimento')
        curso = request.POST.get('curso')
        genero = request.POST.get('genero')
        foto_rosto = request.FILES.get('imagem_rosto')  # Recebe a imagem com o nome correto

        if foto_rosto:
            # Lê a imagem e converte para bytes
            foto_rosto_binaria = foto_rosto.read()

            # Criação do novo aluno com a foto em formato binário
            novo_aluno = Aluno(
                nome_completo=nome_completo,
                email_institucional=email_institucional,
                telefone=telefone,
                endereco=endereco,
                rg=rg,
                registro_matricula=registro_matricula,
                data_nascimento=data_nascimento,
                curso=curso,
                genero=genero,
                foto_rosto=foto_rosto_binaria  # Armazena a imagem como binário
            )
            novo_aluno.save()  # Salva o aluno com a foto no banco
            messages.success(request, "Cadastro de aluno realizado com sucesso!")
            return redirect('home')

        else:
            messages.error(request, "A imagem do rosto não pôde ser capturada.")
            return render(request, 'reconvisual/cadastroalunos.html')
    
    return render(request, 'reconvisual/cadastroalunos.html', {'usuario_nome': request.session.get('usuario_nome', 'Usuário')})

def captura_rosto(request):
    # Captura as imagens em formato binário
    imagens_rosto_binarias = captura_imagem()
    
    if imagens_rosto_binarias:
        return JsonResponse({'imagens_rosto': imagens_rosto_binarias})
    return JsonResponse({'error': 'Erro na captura da imagem'}, status=500)

@login_required
def facemap(request):
    return render(request, 'reconvisual/facemap.html', {'usuario_nome': request.session.get('usuario_nome', 'Usuário')})

@login_required
def sobre(request):
    return render(request, 'reconvisual/sobre.html', {'usuario_nome': request.session.get('usuario_nome', 'Usuário')})

@login_required
def editar(request):
    return render(request, 'reconvisual/editar.html', {'usuario_nome': request.session.get('usuario_nome', 'Usuário')})

@login_required
def editar_aluno(request, aluno_id):
    try:
        aluno = Aluno.objects.get(id=aluno_id)
    except DoesNotExist:
        messages.error(request, "Aluno não encontrado.")
        return redirect('editar')

    if request.method == 'POST':
        # Atualiza os campos com os valores enviados pelo formulário
        aluno.nome_completo = request.POST.get('nome_completo', aluno.nome_completo)
        aluno.email_institucional = request.POST.get('email_institucional', aluno.email_institucional)
        aluno.telefone = request.POST.get('telefone', aluno.telefone)
        aluno.endereco = request.POST.get('endereco', aluno.endereco)
        aluno.rg = request.POST.get('rg', aluno.rg)
        aluno.data_nascimento = request.POST.get('data_nascimento', aluno.data_nascimento)
        aluno.curso = request.POST.get('curso', aluno.curso)
        aluno.genero = request.POST.get('genero', aluno.genero)
        
        # Salva as alterações no banco de dados
        aluno.save()
        messages.success(request, "Cadastro atualizado com sucesso!")
        return redirect('editar')  # Redireciona para a página de edição após salvar

    return render(request, 'reconvisual/editar.html', {'aluno': aluno, 'usuario_nome': request.session.get('usuario_nome', 'Usuário')})

@login_required
def buscar_aluno(request):
    aluno = None
    if request.method == 'GET':
        rm = request.GET.get('rm')
        if rm:
            try:
                aluno = Aluno.objects.get(registro_matricula=rm)
            except DoesNotExist:
                messages.error(request, 'Nenhum aluno encontrado com esse RM.')
    return render(request, 'reconvisual/editar.html', {'usuario_nome': request.session.get('usuario_nome', 'Usuário'), 'aluno': aluno})

def logout(request):
    request.session.flush()
    messages.success(request, "Logout realizado com sucesso!")
    return redirect('index')