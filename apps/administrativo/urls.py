from django.urls import path
from . import views

urlpatterns = [
    path('administrativo/escolas/', views.escolas, name='escolas'),
    path('administrativo/escolas/incluir/', views.escolas_incluir, name='escolas_incluir'),
    path('administrativo/escolas/alterar/<str:id>/', views.escolas_alterar_page, name='escolas_alterar_page'),
    path('administrativo/escolas/alterar/', views.escolas_alterar, name='escolas_alterar'),
    path('administrativo/escolas/excluir/<str:id>/', views.escolas_excluir, name='escolas_excluir'),

    path('administrativo/pessoas/estudantes/<str:id>', views.find_estudante, name='find_estudante'),
    path('administrativo/pessoas/estudantes/', views.pessoas_estudantes, name='pessoas_estudantes'),
    path('administrativo/pessoas/responsaveis/', views.pessoas_responsaveis, name='pessoas_responsaveis'),
    path('administrativo/pessoas/colaboradores/', views.pessoas_colaboradores, name='pessoas_colaboradores'),
    path('administrativo/pessoas/estudantes/incluir/', views.pessoas_estudantes_incluir, name='pessoas_estudantes_incluir'),
    path('administrativo/pessoas/responsaveis/incluir/', views.pessoas_responsaveis_incluir, name='pessoas_responsaveis_incluir'),
    path('administrativo/pessoas/colaboradores/incluir/', views.pessoas_colaboradores_incluir, name='pessoas_colaboradores_incluir'),
    path('administrativo/pessoas/estudantes/alterar/<str:id>/', views.pessoas_estudantes_alterar_page, name='pessoas_estudantes_alterar_page'),
    path('administrativo/pessoas/estudantes/alterar/', views.pessoas_estudantes_alterar, name='pessoas_estudantes_alterar'),
    path('administrativo/pessoas/responsaveis/alterar/<str:id>/', views.pessoas_responsaveis_alterar_page, name='pessoas_responsaveis_alterar_page'),
    path('administrativo/pessoas/responsaveis/alterar/', views.pessoas_responsaveis_alterar, name='pessoas_responsaveis_alterar'),
    path('administrativo/pessoas/colaboradores/alterar/<str:id>/', views.pessoas_colaboradores_alterar_page, name='pessoas_colaboradores_alterar_page'),
    path('administrativo/pessoas/colaboradores/alterar/', views.pessoas_colaboradores_alterar, name='pessoas_colaboradores_alterar'),
    path('administrativo/pessoas/estudantes/excluir/<str:id>/', views.pessoas_estudantes_excluir, name='pessoas_estudantes_excluir'),
    path('administrativo/pessoas/responsaveis/excluir/<str:id>/', views.pessoas_responsaveis_excluir, name='pessoas_responsaveis_excluir'),
    path('administrativo/pessoas/colaboradores/excluir/<str:id>/', views.pessoas_colaboradores_excluir, name='pessoas_colaboradores_excluir'),

    path('administrativo/contratos/', views.contratos, name='contratos'),
    path('administrativo/contratos/incluir/', views.contratos_incluir, name='contratos_incluir'),

    path('administrativo/secretaria/', views.secretaria, name='secretaria'),

    path('administrativo/recepcao/', views.recepcao, name='recepcao'),

    path('administrativo/relatorios/', views.administrativo_relatorios, name='administrativo_relatorios'),
]
