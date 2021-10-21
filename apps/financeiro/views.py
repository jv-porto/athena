from django.shortcuts import render

def bancos(request):
    return render(request, 'financeiro/bancos.html')

def movimentacoes(request):
    return render(request, 'financeiro/movimentacoes.html')

def movimentacoes_incluir(request):
    return render(request, 'financeiro/movimentacoes_incluir.html')

def financeiro_relatorios(request):
    return render(request, 'financeiro/relatorios.html')
