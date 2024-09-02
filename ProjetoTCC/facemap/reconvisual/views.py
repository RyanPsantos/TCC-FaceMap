from django.shortcuts import render

def home(request):
    return render(request, 'reconvisual/home.html')
# 1- Trocar o home para index, aqui sera a pagina de login do usuario
def teste1(request):
    return render(request, 'reconvisual/teste1.html')
# 2- Trocar o teste1 para cadastro, aqui sera a pagina de cadastro que tera um link de acesso pelo login...
def teste2(request):
    return render(request, 'reconvisual/teste2.html')
# 3- Trocar o teste2 para a home do projeto, aonde sera apresentada todas as funçoes e funcionalidades do projeto
def teste3(request):
    return render(request, 'reconvisual/teste3.html')
# 4- Pagina de teste de funçoes hmtls e paginas, assim que conclouida sera feita um Teste 5, e assim por diante ate que todas as telas estejao satisfatorias aos integrantes do projeto


"ATENÇAO aos codigos essencias do Python Django"
"O comando python manage.py runserver e para rodar o servidor e so ira funcionar quando estiver na raiz do projeto, ou seja o facemap"
"Use o comando cd facemap para ir para a raiz do projeto"
"Para saber que esta na raiz do projeto escreva o comando ls, e se estiver na raiz ele ira mostrar as pastas, facemap, reconvisual, db.sqlite3 e manage.py"
"Links para entender como funciona o FRAMEWORK DJANGO, Essencial todos verem para melhor endendimento e diferenças entre o facemap=projeto e reconvisual=aplicativo e funcionalidades do django"



"https://www.youtube.com/watch?v=ZNFVFTqaL60&list=PLLVddSbilcumgeyk0z6ko5U_FYPfbRO2C"
"https://www.youtube.com/watch?v=YW113aC8TII&t=2277s"
"https://www.youtube.com/watch?v=4u0aI-90KnU"
"https://www.youtube.com/watch?v=ahMwu-tJgIY&t=979s"