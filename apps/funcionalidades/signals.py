from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.dispatch import receiver
from .models import Email

@receiver(post_save, sender=Email)
def send_mail_on_create(sender, instance, created, *args, **kwargs):
    if created:
        if instance.tipo == Email.NOVO_USUARIO:
            email_data = {
                'remetente_nome': instance.remetente_nome,
                'remetente_email': instance.remetente_email,
                'destinatarios': instance.destinatarios,
                'assunto': instance.assunto,
                'variaveis': instance.variaveis,
            }
            html_message = render_to_string('funcionalidades/emails/novo_usuario.html', email_data['variaveis'])
            
            connection = get_connection()
            connection.open()
            for destinatario in email_data['destinatarios']:
                email = EmailMultiAlternatives(
                    from_email = f'{email_data["remetente_nome"]} <hermes@thrucode.com.br>',
                    reply_to = [email_data['remetente_email']],
                    to = [destinatario],
                    subject = email_data['assunto'],
                    body = strip_tags(html_message),
                    connection = connection,
                )
                email.attach_alternative(html_message, 'text/html')
                email.send()
            connection.close()
