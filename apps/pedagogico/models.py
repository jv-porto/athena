from django.db import models

class Curso(models.Model):
    id = 0
    descricao = 0
    coordenador = 0
    divisao_periodos = 0
    proposta_pedagogica = 0
    def __str__(self):
        return self.id

class Disciplina(models.Model):
    id = 0
    descricao = 0
    coordenador = 0
    divisao_periodos = 0
    ementa = 0
    def __str__(self):
        return self.id

class Turmas(models.Model):
    id = 0
    descricao = 0
    ano_academico = 0
    disciplinas = 0
    coordenador = 0
    tutor = 0
    curso = 0
    alunos = 0
    turno = 0
    def __str__(self):
        return self.id
