from django.urls import path
from .views import *

urlpatterns = [
    path('escolas/', escolas, name='escolas'),
    path('escolas/incluir/', escolas_incluir, name='escolas_incluir'),
    path('escolas/alterar/<str:id>/', escolas_alterar, name='escolas_alterar'),
    path('escolas/excluir/<str:id>/', escolas_excluir, name='escolas_excluir'),

    path('pessoas/estudantes/', pessoas_estudantes, name='pessoas_estudantes'),
    path('pessoas/estudantes/incluir/', pessoas_estudantes_incluir, name='pessoas_estudantes_incluir'),
    path('pessoas/estudantes/alterar/<str:id>/', pessoas_estudantes_alterar, name='pessoas_estudantes_alterar'),
    path('pessoas/estudantes/excluir/<str:id>/', pessoas_estudantes_excluir, name='pessoas_estudantes_excluir'),

    path('pessoas/responsaveis/', pessoas_responsaveis, name='pessoas_responsaveis'),
    path('pessoas/responsaveis/incluir/', pessoas_responsaveis_incluir, name='pessoas_responsaveis_incluir'),
    path('pessoas/responsaveis/alterar/<str:id>/', pessoas_responsaveis_alterar, name='pessoas_responsaveis_alterar'),
    path('pessoas/responsaveis/excluir/<str:id>/', pessoas_responsaveis_excluir, name='pessoas_responsaveis_excluir'),

    path('pessoas/colaboradores/', pessoas_colaboradores, name='pessoas_colaboradores'),
    path('pessoas/colaboradores/incluir/', pessoas_colaboradores_incluir, name='pessoas_colaboradores_incluir'),
    path('pessoas/colaboradores/alterar/<str:id>/', pessoas_colaboradores_alterar, name='pessoas_colaboradores_alterar'),
    path('pessoas/colaboradores/excluir/<str:id>/', pessoas_colaboradores_excluir, name='pessoas_colaboradores_excluir'),

    path('contratos/', contratos, name='contratos'),
    path('contratos/incluir/', contratos_incluir, name='contratos_incluir'),
    path('contratos/imprimir/<str:id>/', contratos_imprimir, name='contratos_imprimir'),
    path('contratos/digitalizar/<str:id>/', contratos_digitalizar, name='contratos_digitalizar'),
    path('contratos/alterar/<str:id>/', contratos_alterar, name='contratos_alterar'),
    path('contratos/excluir/<str:id>/', contratos_excluir, name='contratos_excluir'),

    path('secretaria/', secretaria, name='secretaria'),

    path('recepcao/', recepcao, name='recepcao'),

    path('relatorios/', administrativo_relatorios, name='administrativo_relatorios'),
]
