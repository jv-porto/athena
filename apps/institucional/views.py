import os, requests, string, secrets
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from athena.custom_storages import MediaStorage
from django.utils.dateparse import parse_date
from django.contrib.auth.models import Group, Permission
from administrativo.models import PessoaEstudante, PessoaResponsavel
from pedagogico.models import Turma, Plataforma
from .models import IntegracaoContaAzul

def empty_input(input):
    return not input.strip()

def add_group_permissions(perms_data, perms_list, module, module_perm_name):
    if perms_data[module] == 'VER':
        perms_list.extend([Permission.objects.get(name=f'Can view {module_perm_name}').id])
    elif perms_data[module] == 'VER_EDITAR':
        perms_list.extend([Permission.objects.get(name=f'Can view {module_perm_name}').id, Permission.objects.get(name=f'Can add {module_perm_name}').id, Permission.objects.get(name=f'Can change {module_perm_name}').id])
    elif perms_data[module] == 'VER_EDITAR_APAGAR':
        perms_list.extend([Permission.objects.get(name=f'Can view {module_perm_name}').id, Permission.objects.get(name=f'Can add {module_perm_name}').id, Permission.objects.get(name=f'Can change {module_perm_name}').id, Permission.objects.get(name=f'Can delete {module_perm_name}').id])

def get_school_id(request):
    if hasattr(request.user, 'pessoaestudante'):
        return request.user.pessoaestudante.escola.id
    elif hasattr(request.user, 'pessoaresponsavel'):
        return request.user.pessoaresponsavel.escola.id
    elif hasattr(request.user, 'pessoacolaborador'):
        return request.user.pessoacolaborador.escola.id
    elif hasattr(request.user, 'escola'):
        return request.user.escola.id



@login_required()
@permission_required('administrativo.view_escola', raise_exception=True)
def cadastro_escolar(request):
    escola = get_school_id(request)
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
    data = {'escola': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/', cookies=cookies, headers=headers).json()}
    return render(request, 'institucional/cadastro_escolar.html', data)


@login_required()
@permission_required('administrativo.change_escola', raise_exception=True)
def cadastro_escolar_alterar(request):
    if request.method == 'GET':
        escola = get_school_id(request)
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        data = {'escola': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/', cookies=cookies, headers=headers).json()}
        return render(request, 'institucional/cadastro_escolar_alterar.html', data)
    elif request.method == 'POST':
        if empty_input(request.POST['address-street']) or empty_input(request.POST['address-neighborhood']) or empty_input(request.POST['address-city']) or empty_input(request.POST['address-state']) or empty_input(request.POST['address-country']):
            messages.error(request, 'Há campos obrigatórios em branco!')
            return redirect('cadastro_escolar_alterar')

        escola = get_school_id(request)

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
            file_extension = str(file.name).split('.')[-1]
            storage = MediaStorage()
            filename = storage.save(f'escolas/logos/logo-{escola}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}.{file_extension}', file)
            school_data['logo'] = storage.url(filename)
        user_data = {
            'email': school_data['email'],
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        user_request = requests.patch(f'http://127.0.0.1:8000/api/usuario/{escola}/', data=user_data, cookies=cookies, headers=headers)
        school_request = requests.patch(f'http://127.0.0.1:8000/api/escola/{escola}/', data=school_data, cookies=cookies, headers=headers)

        return redirect('cadastro_escolar')



@login_required()
@permission_required('institucional.view_usuariospermissoes', raise_exception=True)
def usuarios_permissoes(request):
    escola = get_school_id(request)
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}

    if 'search' in request.GET:
        search = request.GET['search']
        data = {'permissoes': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/usuarios_permissoes/?is_active=true&search={search}', cookies=cookies, headers=headers).json()}
    else:
        data = {'permissoes': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/usuarios_permissoes/?is_active=true', cookies=cookies, headers=headers).json()}

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
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        perms_request = requests.post(f'http://127.0.0.1:8000/api/usuarios_permissoes/', data=perms_data, cookies=cookies, headers=headers)

        return redirect('usuarios_permissoes')


@login_required()
@permission_required('institucional.change_usuariospermissoes', raise_exception=True)
def usuarios_permissoes_alterar(request):
    if request.method == 'GET':
        escola = get_school_id(request)
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        data = {'permissoes': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/usuarios_permissoes/?is_active=true', cookies=cookies, headers=headers).json()}
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
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        perms_request = requests.patch(f'http://127.0.0.1:8000/api/usuarios_permissoes/{perms_data["descricao"]}/', data=perms_data, cookies=cookies, headers=headers)

        return redirect('usuarios_permissoes')


@login_required()
@permission_required('institucional.change_usuariospermissoes', raise_exception=True)
def usuarios_permissoes_excluir(request, id):
    perms_data = {
        'is_active': False,
    }

    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
    perms_request = requests.patch(f'http://127.0.0.1:8000/api/usuarios_permissoes/{id}/',data=perms_data, cookies=cookies, headers=headers)

    return redirect('usuarios_permissoes')



@login_required()
@permission_required('institucional.view_anoacademico', raise_exception=True)
def ano_academico(request):
    escola = get_school_id(request)
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}

    if 'search' in request.GET:
        search = request.GET['search']
        data = {'ano_academico': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/anos_academicos/?deleted=false&search={search}', cookies=cookies, headers=headers).json()}
    else:
        data = {'ano_academico': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/anos_academicos/?deleted=false', cookies=cookies, headers=headers).json()}

    for item in data['ano_academico']:
        item['id'] = item['id'].replace('_', '/')
        item['codigo'] = item['codigo'].replace('_', '/')
        item['inicio'] = parse_date(item['inicio'])
        item['termino'] = parse_date(item['termino'])
    return render(request, 'institucional/ano_academico.html', data)


@login_required()
@permission_required('institucional.add_anoacademico', raise_exception=True)
def ano_academico_incluir(request):
    if request.method == 'GET':
        return render(request, 'institucional/ano_academico_incluir.html')
    elif request.method == 'POST':
        escola = get_school_id(request)
        codigo = request.POST['academic-year-id'].replace('/', '_')

        perms_data = {
            'escola': escola,
            'id': escola + codigo,
            'codigo': codigo,
            'descricao': request.POST['description'],
            'periodicidade': request.POST['periodicity'],
            'inicio': request.POST['start-date'],
            'termino': request.POST['end-date'],
            'deleted': False,
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        perms_request = requests.post(f'http://127.0.0.1:8000/api/ano_academico/', data=perms_data, cookies=cookies, headers=headers)

        return redirect('ano_academico')


@login_required()
@permission_required('institucional.change_anoacademico', raise_exception=True)
def ano_academico_alterar(request, id):
    if request.method == 'GET':
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        data = {'ano_academico': requests.get(f'http://127.0.0.1:8000/api/ano_academico/{id}/', cookies=cookies, headers=headers).json()}
        data['ano_academico']['codigo'] = data['ano_academico']['codigo'].replace('_', '/')
        return render(request, 'institucional/ano_academico_alterar.html', data)
    elif request.method == 'POST':
        perms_data = {
            'descricao': request.POST['description'],
            'periodicidade': request.POST['periodicity'],
            'inicio': request.POST['start-date'],
            'termino': request.POST['end-date'],
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        perms_request = requests.patch(f'http://127.0.0.1:8000/api/ano_academico/{id}/', data=perms_data, cookies=cookies, headers=headers)

        return redirect('ano_academico')


@login_required()
@permission_required('institucional.change_anoacademico', raise_exception=True)
def ano_academico_excluir(request, id):
    perms_data = {
        'deleted': True,
    }

    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
    perms_request = requests.patch(f'http://127.0.0.1:8000/api/ano_academico/{id}/',data=perms_data, cookies=cookies, headers=headers)

    return redirect('ano_academico')



@login_required()
@permission_required('institucional.view_integracoes', raise_exception=True)
def integracoes(request):
    escola = get_school_id(request)
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
    data = {'integracoes': requests.get(f'http://127.0.0.1:8000/api/integracoes/{escola}/', cookies=cookies, headers=headers).json()}
    if data['integracoes']['conta_azul'] == True:
        data['integracaocontaazul'] = IntegracaoContaAzul.objects.get(escola=escola)
    return render(request, 'institucional/integracoes.html', data)


@login_required()
@permission_required('institucional.change_integracoes', raise_exception=True)
def integracoes_alterar(request):
    if request.method == 'GET':
        escola = get_school_id(request)
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        data = {'integracoes': requests.get(f'http://127.0.0.1:8000/api/integracoes/{escola}/', cookies=cookies, headers=headers).json()}
        if data['integracoes']['conta_azul'] == True:
            data['integracaocontaazul'] = IntegracaoContaAzul.objects.get(escola=escola)
        return render(request, 'institucional/integracoes_alterar.html', data)
    elif request.method == 'POST':
        escola = get_school_id(request)

        integrations_data = {
            'conta_azul': 'conta_azul' in request.POST,
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}

        if not IntegracaoContaAzul.objects.filter(escola=escola).exists():
            conta_azul_data = {
                'escola': escola,
                'descricao': escola,
                'is_active': False,
            }
            conta_azul_request = requests.post(f'http://127.0.0.1:8000/api/integracao_conta_azul/', data=conta_azul_data, cookies=cookies, headers=headers)
        else:
            conta_azul_data = {
                'is_active': 'conta_azul' in request.POST,
            }
            conta_azul_request = requests.patch(f'http://127.0.0.1:8000/api/integracao_conta_azul/{escola}/', data=conta_azul_data, cookies=cookies, headers=headers)

        integrations_request = requests.patch(f'http://127.0.0.1:8000/api/integracoes/{escola}/', data=integrations_data, cookies=cookies, headers=headers)

        return redirect('integracoes')


@login_required()
@permission_required('institucional.change_integracaocontaazul', raise_exception=True)
def integracao_conta_azul_ativar(request):
    redirect_uri = 'http://127.0.0.1:8000' + reverse('integracao_conta_azul_token')
    client_id = os.environ['CONTAAZUL_CLIENT_ID']
    state = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(64))

    escola = get_school_id(request)
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
    conta_azul_data = {
        'state': state,
    }
    conta_azul_request = requests.patch(f'http://127.0.0.1:8000/api/integracao_conta_azul/{escola}/', data=conta_azul_data, cookies=cookies, headers=headers)

    return redirect(f'https://api.contaazul.com/auth/authorize?redirect_uri={redirect_uri}&client_id={client_id}&scope=sales&state={state}')


@login_required()
@permission_required('institucional.change_integracaocontaazul', raise_exception=True)
def integracao_conta_azul_token(request):
    escola = get_school_id(request)
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}

    code = request.GET.get('code')
    state = request.GET.get('state')
    db_state = requests.get(f'http://127.0.0.1:8000/api/integracao_conta_azul/{escola}/', cookies=cookies,  headers=headers).json()['state']

    if state != db_state:
        return HttpResponse(status=401)
    else:
        session_request = requests.Session()
        session_request.auth = (os.environ['CONTAAZUL_CLIENT_ID'], os.environ['CONTAAZUL_CLIENT_SECRET'])
        redirect_uri = 'http://127.0.0.1:8000' + reverse('integracao_conta_azul_token')
        conta_azul_token_request = session_request.post(f'https://api.contaazul.com/oauth2/token?grant_type=authorization_code&redirect_uri={redirect_uri}&code={code}')
        token_request_dict = conta_azul_token_request.json()
        token_request_datetime = datetime.now()

        conta_azul_data = {
            'access_token': token_request_dict['access_token'],
            'refresh_token': token_request_dict['refresh_token'],
            'expires_in': token_request_datetime + timedelta(seconds=int(token_request_dict['expires_in'])),
            'is_active': True,
        }
        conta_azul_request = requests.patch(f'http://127.0.0.1:8000/api/integracao_conta_azul/{escola}/', data=conta_azul_data, cookies=cookies, headers=headers)

        if conta_azul_token_request.ok and conta_azul_request.ok:
            messages.success(request, 'A integração foi estabelecida com sucesso')
        else:
            messages.error(request, 'Ocorreu um erro ao realizar a integração')
            return redirect('integracoes')

        ############### INITIAL SYNC ###############
        conta_azul_headers = {'Authorization': f'Bearer {conta_azul_data["access_token"]}'}

        conta_azul_service_data_initial_request = requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/turmas/?deleted=false', cookies=cookies, headers=headers).json()
        for item in conta_azul_service_data_initial_request:
            conta_azul_service = {
                'name': item['descricao'],
                'type': 'PROVIDED',
                'value': float(item['valor_curso'].replace('R$ ', '').replace('.', '').replace(',', '.')),
                #'cost': item[''],
                'code': item['codigo'],
            }
            conta_azul_create_service_request = requests.post(f'https://api.contaazul.com/v1/services/', json=conta_azul_service, headers=conta_azul_headers)
            conta_azul_service_data = {'id_conta_azul': conta_azul_create_service_request.json()['id']}
            conta_azul_service_data_request = requests.patch(f'http://127.0.0.1:8000/api/turma/{item["id"]}/', data=conta_azul_service_data, cookies=cookies, headers=headers)

        conta_azul_contract_data_initial_request = requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/contratos_educacionais/?deleted=false', cookies=cookies, headers=headers).json()
        for item in conta_azul_contract_data_initial_request:
            try:
                if item['estudante_contratante'] == True:
                    contratante = PessoaEstudante.objects.get(pk=item['estudante'])
                    tipo_pessoa = 'estudante'
                elif item['estudante_contratante'] == False:
                    contratante = PessoaResponsavel.objects.get(pk=item['responsavel'])
                    tipo_pessoa = 'responsavel'
                conta_azul_customer = {
                    'name': contratante.nome,
                    'email': contratante.email,
                    'business_phone': contratante.telefone,
                    'mobile_phone': contratante.celular,
                    'person_type': 'NATURAL',
                    'document': contratante.cpf,
                    'identity_document': contratante.rg,
                    'date_of_birth': timezone.make_aware(datetime.combine(contratante.data_nascimento, datetime.min.time())).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                    'address': {
                        'zip_code': contratante.cep,
                        'street': contratante.lougradouro,
                        'number': contratante.numero,
                        'complement': contratante.complemento,
                        'neighborhood': contratante.bairro,
                    }
                }
                conta_azul_customer['date_of_birth'] = conta_azul_customer['date_of_birth'][:-8] + conta_azul_customer['date_of_birth'][-5:]
                conta_azul_create_customer_request = requests.post(f'https://api.contaazul.com/v1/customers/', json=conta_azul_customer, headers=conta_azul_headers)
                conta_azul_customer_data = {'id_conta_azul': conta_azul_create_customer_request.json()['id']}
                conta_azul_customer_data_request = requests.patch(f'http://127.0.0.1:8000/api/pessoas/{tipo_pessoa}/{contratante.id}/', data=conta_azul_customer_data, cookies=cookies, headers=headers)
            except:
                pass

        for item in conta_azul_contract_data_initial_request:
            if item['estudante_contratante'] == True:
                contratante = PessoaEstudante.objects.get(pk=item['estudante'])
                tipo_pessoa = 'estudante'
            elif item['estudante_contratante'] == False:
                contratante = PessoaResponsavel.objects.get(pk=item['responsavel'])
                tipo_pessoa = 'responsavel'
            conta_azul_contract = {
                'number': int(item['codigo']),
                'emission': timezone.make_aware(datetime.combine(datetime.strptime(item['data_inicio_pagamento_curso'], '%Y-%m-%d'), datetime.min.time())).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                'status': 'COMMITTED',
                'customer_id': contratante.id_conta_azul,
                'services': [
                    {
                        'quantity': 1,
                        'service_id': Turma.objects.get(pk=item['turma']).id_conta_azul,
                        'value': round(float(float((Turma.objects.get(pk=item['turma']).valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))*(1-(float(item['desconto_pagamento_curso'].replace('%', '').replace(',', '.'))/100))/int(item['parcelas_pagamento_curso'])),2) + float(3.50*int(item['parcelas_pagamento_curso'])),
                    },
                ],
                #'discount': {
                #  'measure_unit': 'PERCENT',
                #  'rate': float(item['desconto_pagamento_curso'].replace('%', '').replace(',', '.')),
                #},
                'due_day': int(item['dia_pagamento_curso']),
                'duration': int(item['parcelas_pagamento_curso']),
            }
            conta_azul_contract['emission'] = conta_azul_contract['emission'][:-8] + conta_azul_contract['emission'][-5:]
            conta_azul_create_contract_request = requests.post(f'https://api.contaazul.com/v1/contracts/', json=conta_azul_contract, headers=conta_azul_headers)
            conta_azul_contract_data = {'id_conta_azul': conta_azul_create_contract_request.json()['id']}
            conta_azul_contract_data_request = requests.patch(f'http://127.0.0.1:8000/api/contrato_educacional/{item["id"]}/', data=conta_azul_contract_data, cookies=cookies, headers=headers)

        if conta_azul_create_service_request.ok and conta_azul_create_customer_request.ok and conta_azul_create_contract_request.ok:
            conta_azul_data = {
                'is_active': True,
            }
            conta_azul_request = requests.patch(f'http://127.0.0.1:8000/api/integracao_conta_azul/{escola}/', data=conta_azul_data, cookies=cookies, headers=headers)

        return redirect('integracoes')


@login_required()
def integracao_conta_azul_refresh_token(request):
    escola = get_school_id(request)
    integracao_conta_azul = IntegracaoContaAzul.objects.get(escola=escola)
    if (integracao_conta_azul.is_active == True) and (timezone.now() > integracao_conta_azul.expires_in):
        session_request = requests.Session()
        session_request.auth = (os.environ['CONTAAZUL_CLIENT_ID'], os.environ['CONTAAZUL_CLIENT_SECRET'])
        current_refresh_token = integracao_conta_azul.refresh_token
        conta_azul_refresh_token_request = session_request.post(f'https://api.contaazul.com/oauth2/token?grant_type=refresh_token&refresh_token={current_refresh_token}')
        refresh_token_request_dict = conta_azul_refresh_token_request.json()
        refresh_token_request_datetime = datetime.now()

        conta_azul_data = {
            'access_token': refresh_token_request_dict['access_token'],
            'refresh_token': refresh_token_request_dict['refresh_token'],
            'expires_in': refresh_token_request_datetime + timedelta(seconds=int(refresh_token_request_dict ['expires_in'])),
        }
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        conta_azul_request = requests.patch(f'http://127.0.0.1:8000/api/integracao_conta_azul/{escola}/', data=conta_azul_data, cookies=cookies, headers=headers)

        if conta_azul_refresh_token_request.ok and conta_azul_request.ok:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)



@login_required()
@permission_required('pedagogico.view_plataforma', raise_exception=True)
def plataformas(request):
    escola = get_school_id(request)
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}

    if 'search' in request.GET:
        search = request.GET['search']
        data = {'plataformas': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/plataformas/?is_active=true&search={search}', cookies=cookies, headers=headers).json()}
    else:
        data = {'plataformas': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/plataformas/?is_active=true', cookies=cookies, headers=headers).json()}

    return render(request, 'institucional/plataformas.html', data)


@login_required()
@permission_required('pedagogico.add_plataforma', raise_exception=True)
def plataformas_incluir(request):
    if request.method == 'GET':
        return render(request, 'institucional/plataformas_incluir.html')
    if request.method == 'POST':
        def empty_input(input):
            if not input.strip():
                return redirect('plataformas_incluir')
        empty_input(request.POST['description'])
        empty_input(request.POST['link'])

        escola = get_school_id(request)
        if request.POST['code']:
            codigo = request.POST['code']
        else:
            codigo = str(Plataforma.objects.filter(escola=escola).count()+1).zfill(7)

        platform_data = {
            'escola': escola,
            'codigo': codigo,
            'id': str(escola) + codigo,
            'descricao': request.POST['description'],
            'link': request.POST['link'],
            'is_active': True,
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        course_request = requests.post('http://127.0.0.1:8000/api/plataforma/', data=platform_data, cookies=cookies, headers=headers)

        return redirect('plataformas')


@login_required()
@permission_required('pedagogico.change_plataforma', raise_exception=True)
def plataformas_alterar(request, id):
    if request.method == 'GET':
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        data = {'plataforma': requests.get(f'http://127.0.0.1:8000/api/plataforma/{id}/', cookies=cookies, headers=headers).json()}
        return render(request, 'institucional/plataformas_alterar.html', data)
    if request.method == 'POST':
        def empty_input(input):
            if not input.strip():
                return redirect('plataformas_alterar')
        empty_input(request.POST['description'])
        empty_input(request.POST['link'])

        platform_data = {
            'descricao': request.POST['description'],
            'link': request.POST['link'],
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        course_request = requests.patch(f'http://127.0.0.1:8000/api/plataforma/{id}/', data=platform_data, cookies=cookies, headers=headers)

        return redirect('plataformas')


@login_required()
@permission_required('pedagogico.delete_plataforma', raise_exception=True)
def plataformas_excluir(request, id):
    class_data = {
        'is_active': False,
    }

    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
    class_request = requests.patch(f'http://127.0.0.1:8000/api/plataforma/{id}/', data=class_data, cookies=cookies, headers=headers)

    return redirect('plataformas')
