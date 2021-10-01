from django.urls import path
from .views import *

urlpatterns = [
    path('administrativo/escolas/', escolas, name='escolas'),
    path('administrativo/escolas/incluir/', escolas_incluir, name='escolas_incluir'),
    path('administrativo/escolas/alterar/<str:id>/', escolas_alterar_page, name='escolas_alterar_page'),
    path('administrativo/escolas/alterar/', escolas_alterar, name='escolas_alterar'),
    path('administrativo/escolas/excluir/<str:id>/', escolas_excluir, name='escolas_excluir'),

    path('administrativo/pessoas/estudantes/<str:id>', find_estudante, name='find_estudante'),
    path('administrativo/pessoas/estudantes/', pessoas_estudantes, name='pessoas_estudantes'),
    path('administrativo/pessoas/responsaveis/<str:id>', find_responsavel, name='find_responsavel'),
    path('administrativo/pessoas/responsaveis/', pessoas_responsaveis, name='pessoas_responsaveis'),
    path('administrativo/pessoas/colaboradores/', pessoas_colaboradores, name='pessoas_colaboradores'),
    path('administrativo/pessoas/estudantes/incluir/', pessoas_estudantes_incluir, name='pessoas_estudantes_incluir'),
    path('administrativo/pessoas/responsaveis/incluir/', pessoas_responsaveis_incluir, name='pessoas_responsaveis_incluir'),
    path('administrativo/pessoas/colaboradores/incluir/', pessoas_colaboradores_incluir, name='pessoas_colaboradores_incluir'),
    path('administrativo/pessoas/estudantes/alterar/<str:id>/', pessoas_estudantes_alterar_page, name='pessoas_estudantes_alterar_page'),
    path('administrativo/pessoas/estudantes/alterar/', pessoas_estudantes_alterar, name='pessoas_estudantes_alterar'),
    path('administrativo/pessoas/responsaveis/alterar/<str:id>/', pessoas_responsaveis_alterar_page, name='pessoas_responsaveis_alterar_page'),
    path('administrativo/pessoas/responsaveis/alterar/', pessoas_responsaveis_alterar, name='pessoas_responsaveis_alterar'),
    path('administrativo/pessoas/colaboradores/alterar/<str:id>/', pessoas_colaboradores_alterar_page, name='pessoas_colaboradores_alterar_page'),
    path('administrativo/pessoas/colaboradores/alterar/', pessoas_colaboradores_alterar, name='pessoas_colaboradores_alterar'),
    path('administrativo/pessoas/estudantes/excluir/<str:id>/', pessoas_estudantes_excluir, name='pessoas_estudantes_excluir'),
    path('administrativo/pessoas/responsaveis/excluir/<str:id>/', pessoas_responsaveis_excluir, name='pessoas_responsaveis_excluir'),
    path('administrativo/pessoas/colaboradores/excluir/<str:id>/', pessoas_colaboradores_excluir, name='pessoas_colaboradores_excluir'),

    path('administrativo/contratos/', contratos, name='contratos'),
    path('administrativo/contratos/incluir/', contratos_incluir, name='contratos_incluir'),

    path('administrativo/secretaria/', secretaria, name='secretaria'),

    path('administrativo/recepcao/', recepcao, name='recepcao'),

    path('administrativo/relatorios/', administrativo_relatorios, name='administrativo_relatorios'),
]
