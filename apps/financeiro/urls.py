from django.urls import path
from . import views

urlpatterns = [
    path('bancos/', views.bancos, name='bancos'),
    path('movimentacoes/', views.movimentacoes, name='movimentacoes'),
    path('movimentacoes/incluir/', views.movimentacoes_incluir, name='movimentacoes_incluir'),
    path('relatorios/', views.financeiro_relatorios, name='financeiro_relatorios'),
]
