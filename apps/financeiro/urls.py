from django.urls import path
from . import views

urlpatterns = [
    path('financeiro/bancos/', views.bancos, name='bancos'),
    path('financeiro/movimentacoes/', views.movimentacoes, name='movimentacoes'),
    path('financeiro/movimentacoes/incluir/', views.movimentacoes_incluir, name='movimentacoes_incluir'),
    path('financeiro/relatorios/', views.financeiro_relatorios, name='financeiro_relatorios'),
]
