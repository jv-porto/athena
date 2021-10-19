from django.db import models
from django.contrib.auth.models import User
from django.apps import apps

class Escola(models.Model):
    id = models.CharField(primary_key=True, max_length=4)
    cnpj = models.CharField(max_length=18)
    razao_social = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=200)
    email = models.EmailField()
    telefone = models.CharField(max_length=13)
    celular = models.CharField(max_length=13, blank=True)
    site = models.CharField(max_length=200, blank=True)
    logo = models.CharField(max_length=200, blank=True)
    cep = models.CharField(max_length=9)
    lougradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=200, blank=True)
    bairro = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    pais = models.CharField(max_length=200)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    datahora_ultima_alteracao = models.DateTimeField(auto_now=True)
    datahora_cadastro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.id

class ModulosEscola(models.Model):
    escola = models.OneToOneField(Escola, on_delete=models.CASCADE)
    descricao = models.CharField(primary_key=True, max_length=4)
    dashboard = models.BooleanField()
    administrativo_escolas = models.BooleanField()
    administrativo_pessoas_estudantes = models.BooleanField()
    administrativo_pessoas_responsaveis = models.BooleanField()
    administrativo_pessoas_colaboradores = models.BooleanField()
    administrativo_contratos = models.BooleanField()
    administrativo_secretaria = models.BooleanField()
    administrativo_recepcao = models.BooleanField()
    administrativo_relatorios = models.BooleanField()
    pedagogico_cursos = models.BooleanField()
    pedagogico_turmas = models.BooleanField()
    pedagogico_boletim = models.BooleanField()
    pedagogico_diario_classe = models.BooleanField()
    pedagogico_sala_virtual = models.BooleanField()
    pedagogico_vestibulares = models.BooleanField()
    pedagogico_relatorios = models.BooleanField()
    financeiro_bancos = models.BooleanField()
    financeiro_movimentacoes = models.BooleanField()
    financeiro_relatorios = models.BooleanField()
    institucional_cadastro_escolar = models.BooleanField()
    institucional_usuarios_permissoes = models.BooleanField()
    institucional_ano_academico = models.BooleanField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.escola

class PessoaEstudante(models.Model):
    id = models.CharField(primary_key=True, max_length=9)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=5)
    nome = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=12)
    celular = models.CharField(max_length=13)
    telefone = models.CharField(max_length=13, blank=True)
    email = models.EmailField()
    genero = models.CharField(max_length=200)
    cor = models.CharField(max_length=200)
    estado_civil = models.CharField(max_length=200)
    foto = models.CharField(max_length=200, blank=True)
    cep = models.CharField(max_length=9)
    lougradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=200, blank=True)
    bairro = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    pais = models.CharField(max_length=200)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    datahora_ultima_alteracao = models.DateTimeField(auto_now=True)
    datahora_cadastro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.id

class PessoaResponsavel(models.Model):
    id = models.CharField(primary_key=True, max_length=12)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    estudantes = models.ManyToManyField(PessoaEstudante, related_name='responsaveis')
    nome = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=12)
    celular = models.CharField(max_length=13)
    telefone = models.CharField(max_length=13, blank=True)
    email = models.EmailField()
    genero = models.CharField(max_length=200)
    cor = models.CharField(max_length=200)
    estado_civil = models.CharField(max_length=200)
    foto = models.CharField(max_length=200, blank=True)
    cep = models.CharField(max_length=9)
    lougradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=200, blank=True)
    bairro = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    pais = models.CharField(max_length=200)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    datahora_ultima_alteracao = models.DateTimeField(auto_now=True)
    datahora_cadastro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.id

class ContratoTrabalhista(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    valor = models.CharField(max_length=20)
    arquivo = models.CharField(max_length=200)
    digitalizacao = models.CharField(max_length=200, blank=True)
    data_assinatura = models.DateField()
    datahora_ultima_alteracao = models.DateTimeField(auto_now=True)
    datahora_cadastro = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.id

class PessoaColaborador(models.Model):
    id = models.CharField(primary_key=True, max_length=9)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=5)
    nome = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=12)
    celular = models.CharField(max_length=13)
    telefone = models.CharField(max_length=13, blank=True)
    email = models.EmailField()
    genero = models.CharField(max_length=200)
    cor = models.CharField(max_length=200)
    estado_civil = models.CharField(max_length=200)
    foto = models.CharField(max_length=200, blank=True)
    cep = models.CharField(max_length=9)
    lougradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=200, blank=True)
    bairro = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    pais = models.CharField(max_length=200)
    departamento = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    ramal = models.CharField(max_length=10, blank=True)
    admissao = models.DateField()
    demissao = models.DateField(blank=True, null=True)
    remuneracao = models.CharField(max_length=20)
    banco = models.CharField(max_length=4)
    agencia = models.CharField(max_length=5)
    conta = models.CharField(max_length=12)
    contratos = models.ManyToManyField(ContratoTrabalhista, related_name='colaborador', blank=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    datahora_ultima_alteracao = models.DateTimeField(auto_now=True)
    datahora_cadastro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.id

from pedagogico.models import Curso, Turma
class ContratoEducacional(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data_assinatura = models.DateField()
    estudante = models.ForeignKey(PessoaEstudante, on_delete=models.CASCADE)
    responsavel = models.ForeignKey(PessoaResponsavel, on_delete=models.CASCADE, blank=True, null=True)
    estudante_contratante = models.BooleanField()
    desconto_pagamento_matricula = models.CharField(max_length=6)
    data_pagamento_matricula = models.DateField()
    desconto_pagamento_curso = models.CharField(max_length=6)
    parcelas_pagamento_curso = models.CharField(max_length=2)
    dia_pagamento_curso = models.CharField(max_length=2)
    data_inicio_pagamento_curso = models.DateField()
    arquivo_contrato = models.CharField(max_length=200)
    digitalizacao = models.CharField(max_length=200, blank=True)
    datahora_ultima_alteracao = models.DateTimeField(auto_now=True)
    datahora_cadastro = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.id
