from django.shortcuts import render

def cadastro_escolar(request):
    return render(request, 'institucional/cadastro_escolar.html')

def ano_academico(request):
    return render(request, 'institucional/ano_academico.html')

def ano_academico_incluir(request):
    return render(request, 'institucional/ano_academico_incluir.html')

def assinatura(request):
    return render(request, 'institucional/assinatura.html')
