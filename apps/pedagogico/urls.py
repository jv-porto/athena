from django.urls import path
from . import views

urlpatterns = [
    path('cursos/', views.cursos, name='cursos'),
    path('cursos/incluir/', views.cursos_incluir, name='cursos_incluir'),
    path('cursos/alterar/<str:id>/', views.cursos_alterar, name='cursos_alterar'),
    path('cursos/excluir/<str:id>/', views.cursos_excluir, name='cursos_excluir'),
    path('turmas/', views.turmas, name='turmas'),
    path('turmas/incluir/', views.turmas_incluir, name='turmas_incluir'),
    path('turmas/alterar/<str:id>/', views.turmas_alterar, name='turmas_alterar'),
    path('turmas/excluir/<str:id>/', views.turmas_excluir, name='turmas_excluir'),
    path('boletim/', views.boletim, name='boletim'),
    path('diario_de_classe/', views.diario_de_classe, name='diario_de_classe'),
    path('sala_virtual/', views.sala_virtual, name='sala_virtual'),
    path('vestibulares/', views.vestibulares, name='vestibulares'),
    path('relatorios/', views.pedagogico_relatorios, name='pedagogico_relatorios'),
    path('plataforma/<str:id>/', views.plataforma, name='plataforma'),
]
