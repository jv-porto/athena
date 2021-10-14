from django.shortcuts import render
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def calendario(request):
    return render(request, 'funcionalidades/calendario.html')

def mensagens(request):
    return render(request, 'funcionalidades/mensagens.html')

def email(request):
    if request.method == 'GET':
        return render(request, 'funcionalidades/mensagens_email.html')
    if request.method == 'POST':
        mail_data = {
            'tipo': request.POST['type'],
            'remetente_nome': request.POST['sender_name'],
            'remetente_email': request.POST['sender_email'],
            'destinatarios': request.POST['recipients'],
            'assunto': request.POST['subject'],
            'mensagem': request.POST['message'],
            'variaveis': request.POST['variables'],
        }

        connection = get_connection()
        connection.open()
        for destinatario in mail_data['destinatarios']:
            email = EmailMessage(
                from_email = f'{mail_data["remetente_nome"]} <hermes@thrucode.com.br>',
                reply_to = [mail_data['remetente_email']],
                to = [destinatario],
                subject = mail_data['assunto'],
                html_message = render_to_string(mail_data['mensagem'], mail_data['variaveis']),
                plain_message = strip_tags(email['html_message']),
                connection = connection,
            )
            email.content_subtype = 'html'
            email.send()
        connection.close()
