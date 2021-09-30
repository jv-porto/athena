from django.urls import path
from . import views

urlpatterns = [
    path('institucional/cadastro_escolar/', views.cadastro_escolar, name='cadastro_escolar'),
    path('institucional/ano_academico/', views.ano_academico, name='ano_academico'),
    path('institucional/ano_academico/incluir/', views.ano_academico_incluir, name='ano_academico_incluir'),
    path('institucional/assinatura/', views.assinatura, name='assinatura'),
]
