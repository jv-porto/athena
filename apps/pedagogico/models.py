from django.db import models
from django.contrib.postgres import fields
from administrativo.models import Escola, PessoaEstudante, PessoaColaborador
from institucional.models import AnoAcademico

class Disciplina(models.Model):
    id = models.CharField(primary_key=True, max_length=11)
    codigo = models.CharField(max_length=7)
    descricao = models.CharField(max_length=100)
    professores = models.ManyToManyField(PessoaColaborador, related_name='disciplinas', blank=True)
    weekday = fields.ArrayField(models.CharField(max_length=50), default=list)
    horario_inicio = fields.ArrayField(models.TimeField(), default=list)
    horario_termino = fields.ArrayField(models.TimeField(), default=list)
    datahora_ultima_alteracao = models.DateTimeField(auto_now=True)
    datahora_cadastro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.descricao

class Curso(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, max_length=11)
    codigo = models.CharField(max_length=7)
    descricao = models.CharField(max_length=100)
    periodicidade = models.CharField(max_length=100)
    coordenador = models.ForeignKey(PessoaColaborador, on_delete=models.CASCADE, blank=True, null=True)
    proposta_pedagogica = models.CharField(max_length=200, blank=True)
    datahora_ultima_alteracao = models.DateTimeField(auto_now=True)
    datahora_cadastro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.descricao

class Turma(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    ano_academico = models.ForeignKey(AnoAcademico, on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, max_length=11)
    codigo = models.CharField(max_length=7)
    descricao = models.CharField(max_length=100)
    turno = models.CharField(max_length=50)
    vagas = models.CharField(max_length=4)
    tutor = models.ForeignKey(PessoaColaborador, on_delete=models.CASCADE, blank=True, null=True)
    data_inicio = models.DateField(blank=True)
    data_termino = models.DateField(blank=True)
    valor_curso = models.CharField(max_length=15, blank=True)
    parcelamento_curso = models.CharField(max_length=2, blank=True)
    valor_material = models.CharField(max_length=15, blank=True)
    parcelamento_material = models.CharField(max_length=2, blank=True)
    disciplinas = models.ManyToManyField(Disciplina, related_name='turmas', blank=True)
    alunos = models.ManyToManyField(PessoaEstudante, related_name='turmas', blank=True)
    datahora_ultima_alteracao = models.DateTimeField(auto_now=True)
    datahora_cadastro = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    id_conta_azul = models.CharField(max_length=36, blank=True)
    def __str__(self):
        return self.descricao
