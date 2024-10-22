from django.shortcuts import render, redirect
from .models import Professor
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

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
    return render(request, 'reconvisual/cadastro.html')

@login_required
def home(request):
    context = {
        'usuario_nome': request.session.get('usuario_nome', 'Usuário')
    }
    return render(request, 'reconvisual/home.html', context)

@login_required
def cadastroalunos(request):
    context = {
        'usuario_nome': request.session.get('usuario_nome', 'Usuário')
    }
    return render(request, 'reconvisual/cadastroalunos.html', context)

@login_required
def facemap(request):
    context = {
        'usuario_nome': request.session.get('usuario_nome', 'Usuário')
    }
    return render(request, 'reconvisual/facemap.html', context)

@login_required
def sobre(request):
    context = {
        'usuario_nome': request.session.get('usuario_nome', 'Usuário')
    }
    return render(request, 'reconvisual/sobre.html', context)

@login_required
def editar(request):
    context = {
        'usuario_nome': request.session.get('usuario_nome', 'Usuário')
    }
    return render(request, 'reconvisual/editar.html', context)

def logout(request):
    request.session.flush()  # Limpa todas as sessões
    messages.success(request, "Logout realizado com sucesso!")
    return redirect('index')  # Redireciona para a página de login