from django.shortcuts import render
from django.http import HttpResponse

def ver_camera(request):
    return HttpResponse('Ola, tudo bem ?')
