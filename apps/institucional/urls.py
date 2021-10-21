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
]
