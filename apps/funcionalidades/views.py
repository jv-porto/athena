from django.shortcuts import render
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def calendario(request):
    return render(request, 'funcionalidades/calendario.html')

def mensagens(request):
    return render(request, 'funcionalidades/mensagens.html')

def email(request):
    return render(request, 'funcionalidades/email.html')
