from django.shortcuts import render

def index(request):
    return render(request, 'reconvisual/index.html')

def cadastro(request):
    return render(request, 'reconvisual/cadastro.html')

def home(request):
    return render(request, 'reconvisual/home.html')

def cadastroalunos(request):
    return render(request, 'reconvisual/cadastroalunos.html')

def facemap(request):
    return render(request, 'reconvisual/facemap.html')

def sobre(request):
    return render(request, 'reconvisual/sobre.html')

def editarusuario(request):
    return render(request, 'reconvisual/editarusuario.html')

"ATENÇAO aos codigos essencias do Python Django"
"O comando python manage.py runserver e para rodar o servidor e so ira funcionar quando estiver na raiz do projeto, ou seja o facemap"
"Use o comando cd facemap para ir para a raiz do projeto"
"Para saber que esta na raiz do projeto escreva o comando ls, e se estiver na raiz ele ira mostrar as pastas, facemap, reconvisual, db.sqlite3 e manage.py"
"Links para entender como funciona o FRAMEWORK DJANGO, Essencial todos verem para melhor endendimento e diferenças entre o facemap=projeto e reconvisual=aplicativo e funcionalidades do django"



"https://www.youtube.com/watch?v=ZNFVFTqaL60&list=PLLVddSbilcumgeyk0z6ko5U_FYPfbRO2C"
"https://www.youtube.com/watch?v=YW113aC8TII&t=2277s"
"https://www.youtube.com/watch?v=4u0aI-90KnU"
"https://www.youtube.com/watch?v=ahMwu-tJgIY&t=979s"