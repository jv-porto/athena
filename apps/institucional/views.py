import requests
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from athena.custom_storages import MediaStorage
from django.utils.dateparse import parse_date
from django.contrib.auth.models import Group, Permission

def empty_input(input):
    return not input.strip()

def add_group_permissions(perms_data, perms_list, module, module_perm_name):
    if perms_data[module] == 'VER':
        perms_list.extend([Permission.objects.get(name=f'Can view {module_perm_name}').id])
    elif perms_data[module] == 'VER_EDITAR':
        perms_list.extend([Permission.objects.get(name=f'Can view {module_perm_name}').id, Permission.objects.get(name=f'Can add {module_perm_name}').id, Permission.objects.get(name=f'Can change {module_perm_name}').id])
    elif perms_data[module] == 'VER_EDITAR_APAGAR':
        perms_list.extend([Permission.objects.get(name=f'Can view {module_perm_name}').id, Permission.objects.get(name=f'Can add {module_perm_name}').id, Permission.objects.get(name=f'Can change {module_perm_name}').id, Permission.objects.get(name=f'Can delete {module_perm_name}').id])



@login_required()
@permission_required('administrativo.view_escola', raise_exception=True)
def cadastro_escolar(request):
    if request.method == 'GET':
        escola = request.user.escola.id
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        data = {'escola': requests.get(f'https://athena.thrucode.com.br/api/escola/{escola}/', cookies=cookies, headers=headers).json()}
        return render(request, 'institucional/cadastro_escolar.html', data)


@login_required()
@permission_required('administrativo.change_escola', raise_exception=True)
def cadastro_escolar_alterar(request):
    if request.method == 'GET':
        escola = request.user.escola.id
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        data = {'escola': requests.get(f'https://athena.thrucode.com.br/api/escola/{escola}/', cookies=cookies, headers=headers).json()}
        return render(request, 'institucional/cadastro_escolar_alterar.html', data)
    elif request.method == 'POST':
        if empty_input(request.POST['address-street']) or empty_input(request.POST['address-neighborhood']) or empty_input(request.POST['address-city']) or empty_input(request.POST['address-state']) or empty_input(request.POST['address-country']):
            messages.error(request, 'Há campos obrigatórios em branco!')
            return redirect('cadastro_escolar_alterar')

        escola = request.user.escola.id

        school_data = {
            'email': request.POST['email'], 
            'telefone': request.POST['phone-number'], 
            'celular': request.POST['cellphone-number'], 
            'site': request.POST['website'], 
            'cep': request.POST['postal-code'], 
            'lougradouro': request.POST['address-street'], 
            'numero': request.POST['address-number'], 
            'complemento': request.POST['address-complements'], 
            'bairro': request.POST['address-neighborhood'], 
            'cidade': request.POST['address-city'], 
            'estado': request.POST['address-state'], 
            'pais': request.POST['address-country'], 
        }
        if 'logo' in request.FILES:
            file = request.FILES['logo']
            storage = MediaStorage()
            filename = storage.save(f'escolas/logos/logo-{escola}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            school_data['logo'] = storage.url(filename)
        user_data = {
            'email': school_data['email'],
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        user_request = requests.patch(f'https://athena.thrucode.com.br/api/usuario/{escola}/', data=user_data, cookies=cookies, headers=headers)
        school_request = requests.patch(f'https://athena.thrucode.com.br/api/escola/{escola}/', data=school_data, cookies=cookies, headers=headers)

        return redirect('cadastro_escolar')



@login_required()
@permission_required('institucional.view_usuariospermissoes', raise_exception=True)
def usuarios_permissoes(request):
    if request.method == 'GET':
        escola = request.user.escola.id
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        data = {'permissoes': requests.get(f'https://athena.thrucode.com.br/api/escola/{escola}/usuarios_permissoes/?is_active=true', cookies=cookies, headers=headers).json()}
        return render(request, 'institucional/usuarios_permissoes.html', data)


@login_required()
@permission_required('institucional.add_usuariospermissoes', raise_exception=True)
def usuarios_permissoes_incluir(request):
    if request.method == 'GET':
        return render(request, 'institucional/usuarios_permissoes_incluir.html')
    elif request.method == 'POST':
        perms_data = {
            'escola': request.POST['id-escola'],
            'descricao': f'{request.POST["id-escola"]}_' + str(request.POST['description']),
            'is_active': True,
        }
        perms_list = []

        if 'dashboard' in request.POST:
            perms_data['dashboard'] = request.POST['dashboard']

        if 'administrativo_escolas' in request.POST:
            perms_data['administrativo_escolas'] = request.POST['administrativo_escolas']
            add_group_permissions(perms_data, perms_list, 'administrativo_escolas', 'escola')

        if 'administrativo_pessoas_estudantes' in request.POST:
            perms_data['administrativo_pessoas_estudantes'] = request.POST['administrativo_pessoas_estudantes']
            add_group_permissions(perms_data, perms_list, 'administrativo_pessoas_estudantes', 'pessoa estudante')

        if 'administrativo_pessoas_responsaveis' in request.POST:
            perms_data['administrativo_pessoas_responsaveis'] = request.POST['administrativo_pessoas_responsaveis']
            add_group_permissions(perms_data, perms_list, 'administrativo_pessoas_responsaveis', 'pessoa responsavel')

        if 'administrativo_pessoas_colaboradores' in request.POST:
            perms_data['administrativo_pessoas_colaboradores'] = request.POST['administrativo_pessoas_colaboradores']
            add_group_permissions(perms_data, perms_list, 'administrativo_pessoas_colaboradores', 'pessoa colaborador')

        if 'administrativo_contratos' in request.POST:
            perms_data['administrativo_contratos'] = request.POST['administrativo_contratos']
            add_group_permissions(perms_data, perms_list, 'administrativo_contratos', 'contrato')

        if 'administrativo_secretaria' in request.POST:
            perms_data['administrativo_secretaria'] = request.POST['administrativo_secretaria']

        if 'administrativo_recepcao' in request.POST:
            perms_data['administrativo_recepcao'] = request.POST['administrativo_recepcao']

        if 'administrativo_relatorios' in request.POST:
            perms_data['administrativo_relatorios'] = request.POST['administrativo_relatorios']

        if 'pedagogico_cursos' in request.POST:
            perms_data['pedagogico_cursos'] = request.POST['pedagogico_cursos']
            add_group_permissions(perms_data, perms_list, 'pedagogico_cursos', 'curso')

        if 'pedagogico_turmas' in request.POST:
            perms_data['pedagogico_turmas'] = request.POST['pedagogico_turmas']
            add_group_permissions(perms_data, perms_list, 'pedagogico_turmas', 'turma')

        if 'pedagogico_boletim' in request.POST:
            perms_data['pedagogico_boletim'] = request.POST['pedagogico_boletim']

        if 'pedagogico_diario_classe' in request.POST:
            perms_data['pedagogico_diario_classe'] = request.POST['pedagogico_diario_classe']

        if 'pedagogico_sala_virtual' in request.POST:
            perms_data['pedagogico_sala_virtual'] = request.POST['pedagogico_sala_virtual']

        if 'pedagogico_vestibulares' in request.POST:
            perms_data['pedagogico_vestibulares'] = request.POST['pedagogico_vestibulares']

        if 'pedagogico_relatorios' in request.POST:
            perms_data['pedagogico_relatorios'] = request.POST['pedagogico_relatorios']

        if 'financeiro_bancos' in request.POST:
            perms_data['financeiro_bancos'] = request.POST['financeiro_bancos']

        if 'financeiro_movimentacoes' in request.POST:
            perms_data['financeiro_movimentacoes'] = request.POST['financeiro_movimentacoes']

        if 'financeiro_relatorios' in request.POST:
            perms_data['financeiro_relatorios'] = request.POST['financeiro_relatorios']

        if 'institucional_cadastro_escolar' in request.POST:
            perms_data['institucional_cadastro_escolar'] = request.POST['institucional_cadastro_escolar']
            add_group_permissions(perms_data, perms_list, 'institucional_cadastro_escolar', 'escola')

        if 'institucional_usuarios_permissoes' in request.POST:
            perms_data['institucional_usuarios_permissoes'] = request.POST['institucional_usuarios_permissoes']
            add_group_permissions(perms_data, perms_list, 'institucional_usuarios_permissoes', 'usuarios permissoes')

        if 'institucional_ano_academico' in request.POST:
            perms_data['institucional_ano_academico'] = request.POST['institucional_ano_academico']
            add_group_permissions(perms_data, perms_list, 'institucional_ano_academico', 'ano academico')

        group = Group.objects.create(name=perms_data['descricao'])
        perms_data['grupo'] = group.id
        group.permissions.set(perms_list)

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        perms_request = requests.post(f'https://athena.thrucode.com.br/api/usuarios_permissoes/', data=perms_data, cookies=cookies, headers=headers)

        return redirect('usuarios_permissoes')


@login_required()
@permission_required('institucional.change_usuariospermissoes', raise_exception=True)
def usuarios_permissoes_alterar(request):
    if request.method == 'GET':
        escola = request.user.escola.id
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        data = {'permissoes': requests.get(f'https://athena.thrucode.com.br/api/escola/{escola}/usuarios_permissoes/?is_active=true', cookies=cookies, headers=headers).json()}
        return render(request, 'institucional/usuarios_permissoes_alterar.html', data)
    elif request.method == 'POST':
        perms_data = {
            'descricao': f'{request.POST["id-escola"]}_' + str(request.POST['description']),
        }
        perms_list = []

        if 'dashboard' in request.POST:
            perms_data['dashboard'] = request.POST['dashboard']

        if 'administrativo_escolas' in request.POST:
            perms_data['administrativo_escolas'] = request.POST['administrativo_escolas']
            add_group_permissions(perms_data, perms_list, 'administrativo_escolas', 'escola')

        if 'administrativo_pessoas_estudantes' in request.POST:
            perms_data['administrativo_pessoas_estudantes'] = request.POST['administrativo_pessoas_estudantes']
            add_group_permissions(perms_data, perms_list, 'administrativo_pessoas_estudantes', 'pessoa estudante')

        if 'administrativo_pessoas_responsaveis' in request.POST:
            perms_data['administrativo_pessoas_responsaveis'] = request.POST['administrativo_pessoas_responsaveis']
            add_group_permissions(perms_data, perms_list, 'administrativo_pessoas_responsaveis', 'pessoa responsavel')

        if 'administrativo_pessoas_colaboradores' in request.POST:
            perms_data['administrativo_pessoas_colaboradores'] = request.POST['administrativo_pessoas_colaboradores']
            add_group_permissions(perms_data, perms_list, 'administrativo_pessoas_colaboradores', 'pessoa colaborador')

        if 'administrativo_contratos' in request.POST:
            perms_data['administrativo_contratos'] = request.POST['administrativo_contratos']
            add_group_permissions(perms_data, perms_list, 'administrativo_contratos', 'contrato')

        if 'administrativo_secretaria' in request.POST:
            perms_data['administrativo_secretaria'] = request.POST['administrativo_secretaria']

        if 'administrativo_recepcao' in request.POST:
            perms_data['administrativo_recepcao'] = request.POST['administrativo_recepcao']

        if 'administrativo_relatorios' in request.POST:
            perms_data['administrativo_relatorios'] = request.POST['administrativo_relatorios']

        if 'pedagogico_cursos' in request.POST:
            perms_data['pedagogico_cursos'] = request.POST['pedagogico_cursos']
            add_group_permissions(perms_data, perms_list, 'pedagogico_cursos', 'curso')

        if 'pedagogico_turmas' in request.POST:
            perms_data['pedagogico_turmas'] = request.POST['pedagogico_turmas']
            add_group_permissions(perms_data, perms_list, 'pedagogico_turmas', 'turma')

        if 'pedagogico_boletim' in request.POST:
            perms_data['pedagogico_boletim'] = request.POST['pedagogico_boletim']

        if 'pedagogico_diario_classe' in request.POST:
            perms_data['pedagogico_diario_classe'] = request.POST['pedagogico_diario_classe']

        if 'pedagogico_sala_virtual' in request.POST:
            perms_data['pedagogico_sala_virtual'] = request.POST['pedagogico_sala_virtual']

        if 'pedagogico_vestibulares' in request.POST:
            perms_data['pedagogico_vestibulares'] = request.POST['pedagogico_vestibulares']

        if 'pedagogico_relatorios' in request.POST:
            perms_data['pedagogico_relatorios'] = request.POST['pedagogico_relatorios']

        if 'financeiro_bancos' in request.POST:
            perms_data['financeiro_bancos'] = request.POST['financeiro_bancos']

        if 'financeiro_movimentacoes' in request.POST:
            perms_data['financeiro_movimentacoes'] = request.POST['financeiro_movimentacoes']

        if 'financeiro_relatorios' in request.POST:
            perms_data['financeiro_relatorios'] = request.POST['financeiro_relatorios']

        if 'institucional_cadastro_escolar' in request.POST:
            perms_data['institucional_cadastro_escolar'] = request.POST['institucional_cadastro_escolar']
            add_group_permissions(perms_data, perms_list, 'institucional_cadastro_escolar', 'escola')

        if 'institucional_usuarios_permissoes' in request.POST:
            perms_data['institucional_usuarios_permissoes'] = request.POST['institucional_usuarios_permissoes']
            add_group_permissions(perms_data, perms_list, 'institucional_usuarios_permissoes', 'usuarios permissoes')

        if 'institucional_ano_academico' in request.POST:
            perms_data['institucional_ano_academico'] = request.POST['institucional_ano_academico']
            add_group_permissions(perms_data, perms_list, 'institucional_ano_academico', 'ano academico')

        group = Group.objects.get(name=perms_data['descricao'])
        group.permissions.clear()
        group.permissions.set(perms_list)

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        perms_request = requests.patch(f'https://athena.thrucode.com.br/api/usuarios_permissoes/{perms_data["descricao"]}/', data=perms_data, cookies=cookies, headers=headers)

        return redirect('usuarios_permissoes')


@login_required()
@permission_required('institucional.change_usuariospermissoes', raise_exception=True)
def usuarios_permissoes_excluir(request, id):
    perms_data = {
        'is_active': False,
    }

    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
    perms_request = requests.patch(f'https://athena.thrucode.com.br/api/usuarios_permissoes/{id}/',data=perms_data, cookies=cookies, headers=headers)

    return redirect('usuarios_permissoes')



@login_required()
@permission_required('institucional.view_anoacademico', raise_exception=True)
def ano_academico(request):
    escola = request.user.escola.id
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
    data = {'ano_academico': requests.get(f'https://athena.thrucode.com.br/api/escola/{escola}/anos_academicos/?deleted=false', cookies=cookies, headers=headers).json()}
    for item in data['ano_academico']:
        item['id'] = item['id'].replace('_', '/')
        item['inicio'] = parse_date(item['inicio'])
        item['termino'] = parse_date(item['termino'])
    return render(request, 'institucional/ano_academico.html', data)


@login_required()
@permission_required('institucional.add_anoacademico', raise_exception=True)
def ano_academico_incluir(request):
    if request.method == 'GET':
        return render(request, 'institucional/ano_academico_incluir.html')
    elif request.method == 'POST':
        perms_data = {
            'escola': request.user.escola.id,
            'id': request.POST['academic-year-id'].replace('/', '_'),
            'descricao': request.POST['description'],
            'periodicidade': request.POST['periodicity'],
            'inicio': request.POST['start-date'],
            'termino': request.POST['end-date'],
            'deleted': False,
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        perms_request = requests.post(f'https://athena.thrucode.com.br/api/ano_academico/', data=perms_data, cookies=cookies, headers=headers)

        return redirect('ano_academico')


@login_required()
@permission_required('institucional.change_anoacademico', raise_exception=True)
def ano_academico_alterar(request, id):
    if request.method == 'GET':
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        data = {'ano_academico': requests.get(f'https://athena.thrucode.com.br/api/ano_academico/{id}/', cookies=cookies, headers=headers).json()}
        return render(request, 'institucional/ano_academico_alterar.html', data)
    elif request.method == 'POST':
        perms_data = {
            'descricao': request.POST['description'],
            'periodicidade': request.POST['periodicity'],
            'inicio': request.POST['start-date'],
            'termino': request.POST['end-date'],
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
        perms_request = requests.patch(f'https://athena.thrucode.com.br/api/ano_academico/{id}/', data=perms_data, cookies=cookies, headers=headers)

        return redirect('ano_academico')


@login_required()
@permission_required('institucional.change_anoacademico', raise_exception=True)
def ano_academico_excluir(request, id):
    perms_data = {
        'deleted': True,
    }

    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': request.META['HTTP_REFERER']}
    perms_request = requests.patch(f'https://athena.thrucode.com.br/api/ano_academico/{id}/',data=perms_data, cookies=cookies, headers=headers)

    return redirect('ano_academico')
