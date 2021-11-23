from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_escolar/', views.cadastro_escolar, name='cadastro_escolar'),
    path('cadastro_escolar/alterar/', views.cadastro_escolar_alterar, name='cadastro_escolar_alterar'),

    path('usuarios_permissoes/', views.usuarios_permissoes, name='usuarios_permissoes'),
    path('usuarios_permissoes/incluir/', views.usuarios_permissoes_incluir, name='usuarios_permissoes_incluir'),
    path('usuarios_permissoes/alterar/', views.usuarios_permissoes_alterar, name='usuarios_permissoes_alterar'),
    path('usuarios_permissoes/excluir/<str:id>/', views.usuarios_permissoes_excluir, name='usuarios_permissoes_excluir'),

    path('ano_academico/', views.ano_academico, name='ano_academico'),
    path('ano_academico/incluir/', views.ano_academico_incluir, name='ano_academico_incluir'),
    path('ano_academico/alterar/<str:id>/', views.ano_academico_alterar, name='ano_academico_alterar'),
    path('ano_academico/excluir/<str:id>/', views.ano_academico_excluir, name='ano_academico_excluir'),

    path('integracoes/', views.integracoes, name='integracoes'),
    path('integracoes/alterar/', views.integracoes_alterar, name='integracoes_alterar'),
    path('integracoes/conta_azul/ativar/', views.integracao_conta_azul_ativar, name='integracao_conta_azul_ativar'),
    path('integracoes/conta_azul/token/', views.integracao_conta_azul_token, name='integracao_conta_azul_token'),
    path('integracoes/conta_azul/refresh_token/', views.integracao_conta_azul_refresh_token, name='integracao_conta_azul_refresh_token'),

    path('plataformas/', views.plataformas, name='plataformas'),
    path('plataformas/incluir/', views.plataformas_incluir, name='plataformas_incluir'),
    path('plataformas/alterar/<str:id>/', views.plataformas_alterar, name='plataformas_alterar'),
    path('plataformas/excluir/<str:id>/', views.plataformas_excluir, name='plataformas_excluir'),
]
