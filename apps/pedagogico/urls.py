from django.urls import path
from . import views

urlpatterns = [
    path('pedagogico/cursos/', views.cursos, name='cursos'),
    path('pedagogico/cursos/incluir/', views.cursos_incluir, name='cursos_incluir'),
    path('pedagogico/disciplinas/', views.disciplinas, name='disciplinas'),
    path('pedagogico/disciplinas/incluir/', views.disciplinas_incluir, name='disciplinas_incluir'),
    path('pedagogico/turmas/', views.turmas, name='turmas'),
    path('pedagogico/turmas/incluir/', views.turmas_incluir, name='turmas_incluir'),
    path('pedagogico/boletim/', views.boletim, name='boletim'),
    path('pedagogico/diario_de_classe/', views.diario_de_classe, name='diario_de_classe'),
    path('pedagogico/sala_virtual/', views.sala_virtual, name='sala_virtual'),
    path('pedagogico/vestibulares/', views.vestibulares, name='vestibulares'),
    path('pedagogico/relatorios/', views.pedagogico_relatorios, name='pedagogico_relatorios'),
]
