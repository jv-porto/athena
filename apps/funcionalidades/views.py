from django.shortcuts import render

def calendario(request):
    return render(request, 'funcionalidades/calendario.html')

def mensagens(request):
    return render(request, 'funcionalidades/mensagens.html')
