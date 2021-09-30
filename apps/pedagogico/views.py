from django.shortcuts import render

def cursos(request):
    return render(request, 'pedagogico/cursos.html')

def cursos_incluir(request):
    return render(request, 'pedagogico/cursos_incluir.html')

def disciplinas(request):
    return render(request, 'pedagogico/disciplinas.html')

def disciplinas_incluir(request):
    return render(request, 'pedagogico/disciplinas_incluir.html')

def turmas(request):
    return render(request, 'pedagogico/turmas.html')

def turmas_incluir(request):
    return render(request, 'pedagogico/turmas_incluir.html')

def boletim(request):
    return render(request, 'pedagogico/boletim.html')

def diario_de_classe(request):
    return render(request, 'pedagogico/diario_de_classe.html')

def sala_virtual(request):
    return render(request, 'pedagogico/sala_virtual.html')

def vestibulares(request):
    return render(request, 'pedagogico/vestibulares.html')

def pedagogico_relatorios(request):
    return render(request, 'pedagogico/relatorios.html')
