from django.db import models
from django.contrib.postgres import fields

class Email(models.Model):
    PERSONALIZADO, NOVO_USUARIO, ESQUECI_MINHA_SENHA = 'PERSONALIZADO', 'NOVO_USUARIO', 'ESQUECI_MINHA_SENHA'
    tipo_opcoes = (
        (PERSONALIZADO, 'Personalizado'),
        (NOVO_USUARIO, 'Novo usuário'),
        (ESQUECI_MINHA_SENHA, 'Esqueci minha senha'),
    )

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50, choices=tipo_opcoes)
    remetente_nome = models.CharField(max_length=50)
    remetente_email = models.EmailField(blank=True, null=True)
    destinatarios = fields.ArrayField(models.EmailField())
    ccs = fields.ArrayField(models.EmailField(), default=list)
    assunto = models.CharField(max_length=100)
    mensagem_txt = models.TextField(blank=True, null=True)
    mensagem_html = models.CharField(max_length=100, blank=True, null=True)
    variaveis = models.JSONField(blank=True, null=True, default=dict)
    anexos = models.CharField(max_length=200, blank=True, null=True)
