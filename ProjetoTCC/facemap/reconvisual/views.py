from django.shortcuts import render, redirect
from .models import Professor, Aluno
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from mongoengine.errors import DoesNotExist
from django.http import JsonResponse
import cv2
import numpy as np

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

        try:
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
            )
            novo_aluno.save()

            messages.success(request, "Cadastro de aluno realizado com sucesso!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Erro ao cadastrar aluno: {e}")

    return render(request, 'reconvisual/cadastroalunos.html', {'usuario_nome': request.session.get('usuario_nome', 'Usuário')})

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