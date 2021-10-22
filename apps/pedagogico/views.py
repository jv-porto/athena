import requests
from datetime import datetime
from django.contrib import messages
from athena.custom_storages import MediaStorage
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from .models import Curso, Disciplina, Turma
from administrativo.models import PessoaColaborador
from institucional.models import AnoAcademico

def empty_input(input):
    return not input.strip()



@login_required()
@permission_required('pedagogico.view_curso', raise_exception=True)
def cursos(request):
    if request.user.pessoaestudante:
        escola = request.user.pessoaestudante.escola.id
    elif request.user.pessoaresponsavel:
        escola = request.user.pessoaresponsavel.escola.id
    elif request.user.pessoacolaborador:
        escola = request.user.pessoacolaborador.escola.id
    elif request.user.escola:
        escola = request.user.escola.id
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
    data = {'cursos': requests.get(f'https://athena.thrucode.com.br/api/escola/{escola}/cursos/?is_active=true', cookies=cookies, headers=headers).json()}
    return render(request, 'pedagogico/cursos.html', data)


@login_required()
@permission_required('pedagogico.add_curso', raise_exception=True)
def cursos_incluir(request):
    if request.method == 'GET':
        return render(request, 'pedagogico/cursos_incluir.html')
    if request.method == 'POST':
        def empty_input(input):
            if not input.strip():
                return redirect('cursos_incluir')
        empty_input(request.POST['description'])

        if request.user.pessoaestudante:
            escola = request.user.pessoaestudante.escola.id
        elif request.user.pessoaresponsavel:
            escola = request.user.pessoaresponsavel.escola.id
        elif request.user.pessoacolaborador:
            escola = request.user.pessoacolaborador.escola.id
        elif request.user.escola:
            escola = request.user.escola.id
        if request.POST['code']:
            codigo = request.POST['code']
        else:
            codigo = str(Curso.objects.filter(escola=escola).count()+1).zfill(7)
        
        course_data = {
            'escola': escola,
            'id': str(escola) + codigo,
            'descricao': request.POST['description'],
            'periodicidade': request.POST['periodicity'],
            'valor_curso': request.POST['cost'],
            'parcelamento_curso': request.POST['installments'],
            'valor_material': request.POST['material-cost'],
            'parcelamento_material': request.POST['material-installments'],
            'data_final_cancelamento': request.POST['cancel-date'],
            'disciplinas': [],
            'is_active': True,
        }
        if 'syllabus' in request.FILES:
            file = request.FILES['syllabus']
            storage = MediaStorage()
            filename = storage.save(f'cursos/{course_data["id"]}/proposta_pedagogica/proposta_pedagogica-{course_data["id"]}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            course_data['proposta_pedagogica'] = storage.url(filename)
        if request.POST['coordinator']:
            if PessoaColaborador.objects.filter(pk=request.POST['coordinator']).exists():
                course_data['coordenador'] = request.POST['coordinator']
            else:
                messages.error(request, 'O ID do coordenador está incorreto!')
                return redirect('cursos_incluir')

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}

        i = 0
        while i <= 14:
            try:
                if request.POST[f'subject-code-{i}']:
                    codigo_disciplina = request.POST[f'subject-code-{i}']
                else:
                    codigo_disciplina = str(Disciplina.objects.filter(escola=escola).count()+1).zfill(7)
                subjects_data = {
                'id': str(escola) + codigo_disciplina,
                'descricao': request.POST[f'subject-description-{i}'],
                'weekday': request.POST[f'subject-weekday-{i}'],
                'horario_inicio': request.POST[f'subject-start-time-{i}'],
                'horario_termino': request.POST[f'subject-end-time-{i}'],
                }
                if PessoaColaborador.objects.filter(pk=request.POST[f'subject-teacher-{i}']).exists():
                    subjects_data['professores'] = request.POST[f'subject-teacher-{i}']
                else:
                    messages.error(request, 'O ID do professor está incorreto!')
                    return redirect('cursos_incluir')

                subjects_request = requests.post(f'https://athena.thrucode.com.br/api/disciplina/', data=subjects_data, cookies=cookies, headers=headers)
                course_data['disciplinas'].append(subjects_data['id'])

                i += 1
            except:
                i += 1

        course_request = requests.post('https://athena.thrucode.com.br/api/curso/', data=course_data, cookies=cookies, headers=headers)

        return redirect('cursos')


@login_required()
@permission_required('pedagogico.change_curso', raise_exception=True)
def cursos_alterar(request, id):
    if request.method == 'GET':
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        data = {'curso': requests.get(f'https://athena.thrucode.com.br/api/curso/{id}/', cookies=cookies, headers=headers).json(), 'disciplinas': []}
        for disciplina in data['curso']['disciplinas']:
            data['disciplinas'].append(Disciplina.objects.get(pk=disciplina))
        return render(request, 'pedagogico/cursos_alterar.html', data)
    if request.method == 'POST':
        def empty_input(input):
            if not input.strip():
                return redirect('cursos_alterar')
        empty_input(request.POST['description'])

        if request.user.pessoaestudante:
            escola = request.user.pessoaestudante.escola.id
        elif request.user.pessoaresponsavel:
            escola = request.user.pessoaresponsavel.escola.id
        elif request.user.pessoacolaborador:
            escola = request.user.pessoacolaborador.escola.id
        elif request.user.escola:
            escola = request.user.escola.id
        
        course_data = {
            'descricao': request.POST['description'],
            'periodicidade': request.POST['periodicity'],
            'valor_curso': request.POST['cost'],
            'parcelamento_curso': request.POST['installments'],
            'valor_material': request.POST['material-cost'],
            'parcelamento_material': request.POST['material-installments'],
            'data_final_cancelamento': request.POST['cancel-date'],
            'disciplinas': [],
            'is_active': True,
        }
        if 'syllabus' in request.FILES:
            file = request.FILES['syllabus']
            storage = MediaStorage()
            filename = storage.save(f'cursos/{id}/proposta_pedagogica/proposta_pedagogica-{id}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            course_data['proposta_pedagogica'] = storage.url(filename)
        if request.POST['coordinator']:
            if PessoaColaborador.objects.filter(pk=request.POST['coordinator']).exists():
                course_data['coordenador'] = request.POST['coordinator']
            else:
                messages.error(request, 'O ID do coordenador está incorreto!')
                return redirect('cursos_alterar')

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        course_request = requests.patch(f'https://athena.thrucode.com.br/api/curso/{id}/', data=course_data, cookies=cookies, headers=headers)
        curso = Curso.objects.get(pk=id)

        i = 0
        while i <= 14:
            try:
                if request.POST[f'subject-code-{i}']:
                    codigo_disciplina = request.POST[f'subject-code-{i}']
                else:
                    codigo_disciplina = str(Disciplina.objects.filter(escola=escola).count()+1).zfill(7)
                if len(codigo_disciplina) == 7:
                    id_disciplina = str(escola) + codigo_disciplina
                elif len(codigo_disciplina) == 11:
                    id_disciplina = codigo_disciplina
                else:
                    messages.error(request, 'O ID da disciplina está incorreto!')
                    return redirect('cursos_alterar')

                subjects_data = {
                'id': id_disciplina,
                'descricao': request.POST[f'subject-description-{i}'],
                'weekday': request.POST[f'subject-weekday-{i}'],
                'horario_inicio': request.POST[f'subject-start-time-{i}'],
                'horario_termino': request.POST[f'subject-end-time-{i}'],
                }
                if PessoaColaborador.objects.filter(pk=request.POST[f'subject-teacher-{i}']).exists():
                    professor = request.POST[f'subject-teacher-{i}']
                else:
                    messages.error(request, 'O ID do professor está incorreto!')
                    return redirect('cursos_alterar')

                subjects_request = requests.post(f'https://athena.thrucode.com.br/api/disciplina/', data=subjects_data, cookies=cookies, headers=headers)
                if not subjects_request.ok:
                    subjects_request = requests.patch(f'https://athena.thrucode.com.br/api/disciplina/{id}/', data=subjects_data, cookies=cookies, headers=headers)
                disciplina = Disciplina.objects.get(pk=subjects_data)
                disciplina.professores.add(professor)
                curso.disciplinas.add(disciplina)

                i += 1
            except:
                i += 1

        return redirect('cursos')


@login_required()
@permission_required('pedagogico.delete_curso', raise_exception=True)
def cursos_excluir(request, id):
    course_data = {
        'is_active': False,
    }

    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
    course_request = requests.patch(f'https://athena.thrucode.com.br/api/curso/{id}/', data=course_data, cookies=cookies, headers=headers)

    return redirect('cursos')



@login_required()
@permission_required('pedagogico.view_turma', raise_exception=True)
def turmas(request):
    if request.user.pessoaestudante:
        escola = request.user.pessoaestudante.escola.id
    elif request.user.pessoaresponsavel:
        escola = request.user.pessoaresponsavel.escola.id
    elif request.user.pessoacolaborador:
        escola = request.user.pessoacolaborador.escola.id
    elif request.user.escola:
        escola = request.user.escola.id
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
    data = {'turmas': requests.get(f'https://athena.thrucode.com.br/api/escola/{escola}/turmas/?deleted=false', cookies=cookies, headers=headers).json()}
    for item in data['turmas']:
        item['ano_academico'] = item['ano_academico'].replace('_', '/')
    return render(request, 'pedagogico/turmas.html', data)


@login_required()
@permission_required('pedagogico.add_turma', raise_exception=True)
def turmas_incluir(request):
    if request.method == 'GET':
        return render(request, 'pedagogico/turmas_incluir.html')
    if request.method == 'POST':
        if empty_input(request.POST['description']):
            messages.error(request, 'Há campos obrigatórios em branco!')
            return redirect('turmas_incluir')

        if request.user.pessoaestudante:
            escola = request.user.pessoaestudante.escola.id
        elif request.user.pessoaresponsavel:
            escola = request.user.pessoaresponsavel.escola.id
        elif request.user.pessoacolaborador:
            escola = request.user.pessoacolaborador.escola.id
        elif request.user.escola:
            escola = request.user.escola.id
        if request.POST['code']:
            codigo = request.POST['code']
        else:
            codigo = str(Turma.objects.filter(escola=escola).count()+1).zfill(7)
        
        class_data = {
            'escola': escola,
            'id': str(escola) + codigo,
            'descricao': request.POST['description'],
            'turno': request.POST['shift'],
            'vagas': request.POST['slots'],
            'data_inicio': request.POST['start-date'],
            'data_termino': request.POST['end-date'],
            'deleted': False,
        }
        if Curso.objects.filter(pk=request.POST['course-id']).exists():
            class_data['curso'] = request.POST['course-id']
        else:
            messages.error(request, 'O ID do curso está incorreto!')
            return redirect('turmas_incluir')
        if AnoAcademico.objects.filter(pk=request.POST['academic-year-id'].replace('/', '_')).exists():
            ano_academico = AnoAcademico.objects.get(pk=request.POST['academic-year-id'].replace('/', '_'))
            class_data['ano_academico'] = ano_academico.id
        else:
            messages.error(request, 'O ID do ano acadêmico está incorreto!')
            return redirect('turmas_incluir')
        if request.POST['start-date']:
            class_data['data_inicio'] = request.POST['start-date']
        else:
            class_data['data_inicio'] = ano_academico.data_inicio
        if request.POST['end-date']:
            class_data['data_termino'] = request.POST['end-date']
        else:
            class_data['data_termino'] = ano_academico.data_termino
        if request.POST['tutor']:
            if PessoaColaborador.objects.filter(pk=request.POST['tutor']).exists():
                class_data['tutor'] = request.POST['tutor']
            else:
                messages.error(request, 'O ID do tutor está incorreto!')
                return redirect('turmas_incluir')

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        course_request = requests.post('https://athena.thrucode.com.br/api/turma/', data=class_data, cookies=cookies, headers=headers)

        return redirect('turmas')


@login_required()
@permission_required('pedagogico.change_turma', raise_exception=True)
def turmas_alterar(request, id):
    if request.method == 'GET':
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        data = {'turma': requests.get(f'https://athena.thrucode.com.br/api/turma/{id}/', cookies=cookies, headers=headers).json()}
        data['turma']['ano_academico'] = data['turma']['ano_academico'].replace('_', '/')
        return render(request, 'pedagogico/turmas_alterar.html', data)
    if request.method == 'POST':
        if empty_input(request.POST['description']):
            messages.error(request, 'Há campos obrigatórios em branco!')
            return redirect('turmas_alterar')

        class_data = {
            'descricao': request.POST['description'],
            'turno': request.POST['shift'],
            'vagas': request.POST['slots'],
            'data_inicio': request.POST['start-date'],
            'data_termino': request.POST['end-date'],
        }
        if Curso.objects.filter(pk=request.POST['course-id']).exists():
            class_data['curso'] = request.POST['course-id']
        else:
            messages.error(request, 'O ID do curso está incorreto!')
            return redirect('turmas_alterar')
        if AnoAcademico.objects.filter(pk=request.POST['academic-year-id'].replace('/', '_')).exists():
            class_data['ano_academico'] = request.POST['academic-year-id'].replace('/', '_')
        else:
            messages.error(request, 'O ID do ano acadêmico está incorreto!')
            return redirect('turmas_alterar')
        if request.POST['tutor']:
            if PessoaColaborador.objects.filter(pk=request.POST['tutor']).exists():
                class_data['tutor'] = request.POST['tutor']
            else:
                messages.error(request, 'O ID do tutor está incorreto!')
                return redirect('turmas_alterar')

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        course_request = requests.patch(f'https://athena.thrucode.com.br/api/turma/{id}/', data=class_data, cookies=cookies, headers=headers)

        return redirect('turmas')


@login_required()
@permission_required('pedagogico.delete_turma', raise_exception=True)
def turmas_excluir(request, id):
    class_data = {
        'deleted': True,
    }

    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
    class_request = requests.patch(f'https://athena.thrucode.com.br/api/turma/{id}/', data=class_data, cookies=cookies, headers=headers)

    return redirect('turmas')



@login_required()
def boletim(request):
    return render(request, 'pedagogico/boletim.html')



@login_required()
def diario_de_classe(request):
    return render(request, 'pedagogico/diario_de_classe.html')



@login_required()
def sala_virtual(request):
    return render(request, 'pedagogico/sala_virtual.html')



@login_required()
def vestibulares(request):
    return render(request, 'pedagogico/vestibulares.html')



@login_required()
def pedagogico_relatorios(request):
    return render(request, 'pedagogico/relatorios.html')
