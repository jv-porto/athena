from django.db import models
from django.contrib.auth.models import Group
from administrativo.models import Escola

class AnoAcademico(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, max_length=10)
    codigo = models.CharField(max_length=6)
    descricao = models.CharField(max_length=100)
    periodicidade = models.CharField(max_length=100)
    inicio = models.DateField()
    termino = models.DateField()
    datahora_ultima_alteracao = models.DateTimeField(auto_now=True)
    datahora_cadastro = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.descricao

class UsuariosPermissoes(models.Model):
    NENHUMA, VER, VER_EDITAR, VER_EDITAR_APAGAR = 'NENHUMA', 'VER', 'VER_EDITAR', 'VER_EDITAR_APAGAR'
    perms_opcoes = (
        (NENHUMA, 'Nenhuma'),
        (VER, 'Ver'),
        (VER_EDITAR, 'Ver e editar'),
        (VER_EDITAR_APAGAR, 'Ver, editar e apagar'),
    )

    grupo = models.OneToOneField(Group, on_delete=models.CASCADE)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    descricao = models.CharField(primary_key=True, max_length=50)
    dashboard = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    administrativo_escolas = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    administrativo_pessoas_estudantes = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    administrativo_pessoas_responsaveis = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    administrativo_pessoas_colaboradores = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    administrativo_contratos = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    administrativo_secretaria = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    administrativo_recepcao = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    administrativo_relatorios = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    pedagogico_cursos = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    pedagogico_turmas = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    pedagogico_boletim = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    pedagogico_diario_classe = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    pedagogico_sala_virtual = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    pedagogico_vestibulares = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    pedagogico_relatorios = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    financeiro_bancos = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    financeiro_movimentacoes = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    financeiro_relatorios = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    institucional_cadastro_escolar = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    institucional_usuarios_permissoes = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    institucional_ano_academico = models.CharField(max_length=50, choices=perms_opcoes, default=NENHUMA)
    datahora_ultima_alteracao = models.DateTimeField(auto_now=True)
    datahora_cadastro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.descricao

class Integracoes(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    descricao = models.CharField(primary_key=True, max_length=4)
    conta_azul = models.BooleanField(default=False)
    datahora_ultima_alteracao = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.descricao

class IntegracaoContaAzul(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='integracaocontaazul')
    descricao = models.CharField(primary_key=True, max_length=4)
    state = models.CharField(max_length=100, blank=True)
    access_token = models.CharField(max_length=100, blank=True)
    refresh_token = models.CharField(max_length=100, blank=True)
    expires_in = models.DateTimeField(blank=True, null=True)
    datahora_ultima_alteracao = models.DateTimeField(auto_now=True)
    datahora_cadastro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.descricao
