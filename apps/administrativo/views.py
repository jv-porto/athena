import requests, locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from athena.custom_storages import MediaStorage
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User
from administrativo.models import Escola, PessoaEstudante, PessoaResponsavel, PessoaColaborador, ContratoEducacional
from pedagogico.models import Curso, Turma
from institucional.models import IntegracaoContaAzul
from .modules.numeroExtenso import dExtenso
from .contratos import *

def empty_input(input):
    return not input.strip()

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
def escolas(request):
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}

    if 'search' in request.GET:
        search = request.GET['search']
        data = {'escolas': requests.get(f'http://127.0.0.1:8000/api/escola/?search={search}', cookies=cookies, headers=headers).json()}
    else:
        data = {'escolas': requests.get('http://127.0.0.1:8000/api/escola/', cookies=cookies, headers=headers).json()}
    
    return render(request, 'administrativo/escolas.html', data)


@login_required()
@permission_required('administrativo.add_escola', raise_exception=True)
def escolas_incluir(request):
    if request.method == 'GET':
        return render(request, 'administrativo/escolas_incluir.html')
    elif request.method == 'POST':
        if empty_input(request.POST['corporate-name']) or empty_input(request.POST['trading-name']) or empty_input(request.POST['address-street']) or empty_input(request.POST['address-neighborhood']) or empty_input(request.POST['address-city']) or empty_input(request.POST['address-state']) or empty_input(request.POST['address-country']):
            messages.error(request, 'Há campos obrigatórios em branco!')
            return redirect('escolas_incluir')
        
        if request.POST['school-id']:
            id_escola = request.POST['school-id']
        else:
            id_escola = f'{str(Escola.objects.all().count()).zfill(4)}'

        school_data = {
            'id': id_escola,
            'cnpj': request.POST['cnpj'], 
            'razao_social': request.POST['corporate-name'], 
            'nome_fantasia': request.POST['trading-name'], 
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
            'is_active': True,
        }
        if 'logo' in request.FILES:
            file = request.FILES['logo']
            storage = MediaStorage()
            filename = storage.save(f'escolas/{school_data["id"]}/logos/logo-{school_data["id"]}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            school_data['logo'] = storage.url(filename)
        if 'signature' in request.FILES:
            file = request.FILES['signature']
            storage = MediaStorage()
            filename = storage.save(f'escolas/{school_data["id"]}/assinaturas/assinatura-{school_data["id"]}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            school_data['assinatura'] = storage.url(filename)
        user_data = {
            'username': school_data['id'],
            'first_name': school_data['nome_fantasia'],
            'email': school_data['email'],
            'password': '0',
            'is_active': True,
        }
        perms_data = {
            'escola': school_data['id'],
            'descricao': school_data['id'],
            'dashboard': 'dashboard' in request.POST,
            'administrativo_escolas': 'administrativo_escolas' in request.POST,
            'administrativo_pessoas_estudantes': 'administrativo_pessoas_estudantes' in request.POST,
            'administrativo_pessoas_responsaveis': 'administrativo_pessoas_responsaveis' in request.POST,
            'administrativo_pessoas_colaboradores': 'administrativo_pessoas_colaboradores' in request.POST,
            'administrativo_contratos': 'administrativo_contratos' in request.POST,
            'administrativo_secretaria': 'administrativo_secretaria' in request.POST,
            'administrativo_recepcao': 'administrativo_recepcao' in request.POST,
            'administrativo_relatorios': 'administrativo_relatorios' in request.POST,
            'pedagogico_cursos': 'pedagogico_cursos' in request.POST,
            'pedagogico_turmas': 'pedagogico_turmas' in request.POST,
            'pedagogico_boletim': 'pedagogico_boletim' in request.POST,
            'pedagogico_diario_classe': 'pedagogico_diario_classe' in request.POST,
            'pedagogico_sala_virtual': 'pedagogico_sala_virtual' in request.POST,
            'pedagogico_vestibulares': 'pedagogico_vestibulares' in request.POST,
            'pedagogico_relatorios': 'pedagogico_relatorios' in request.POST,
            'financeiro_bancos': 'financeiro_bancos' in request.POST,
            'financeiro_movimentacoes': 'financeiro_movimentacoes' in request.POST,
            'financeiro_relatorios': 'financeiro_relatorios' in request.POST,
            'institucional_cadastro_escolar': 'institucional_cadastro_escolar' in request.POST,
            'institucional_usuarios_permissoes': 'institucional_usuarios_permissoes' in request.POST,
            'institucional_ano_academico': 'institucional_ano_academico' in request.POST,
            'institucional_integracoes': 'institucional_integracoes' in request.POST,
            'is_active': True,
        }
        integration_data = {
            'escola': school_data['id'],
            'descricao': school_data['id'],
            'is_active': True,
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        user_request = requests.post('http://127.0.0.1:8000/api/usuario/', data=user_data, cookies=cookies, headers=headers)
        school_data['usuario'] = User.objects.get(username=user_data['username']).id
        school_request = requests.post('http://127.0.0.1:8000/api/escola/', data=school_data, cookies=cookies, headers=headers)
        perms_request = requests.post(f'http://127.0.0.1:8000/api/modulos_escola/', data=perms_data, cookies=cookies, headers=headers)
        integration_request = requests.post(f'http://127.0.0.1:8000/api/integracoes/', data=integration_data, cookies=cookies, headers=headers)

        return redirect('escolas')


@login_required()
@permission_required('administrativo.change_escola', raise_exception=True)
def escolas_alterar(request, id):
    if request.method == 'GET':
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        data = {'escola': requests.get(f'http://127.0.0.1:8000/api/escola/{id}/', cookies=cookies, headers=headers).json(), 'modules': requests.get(f'http://127.0.0.1:8000/api/modulos_escola/{id}/', cookies=cookies, headers=headers).json()}
        return render(request, 'administrativo/escolas_alterar.html', data)
    elif request.method == 'POST':
        if empty_input(request.POST['corporate-name']) or empty_input(request.POST['trading-name']) or empty_input(request.POST['address-street']) or empty_input(request.POST['address-neighborhood']) or empty_input(request.POST['address-city']) or empty_input(request.POST['address-state']) or empty_input(request.POST['address-country']):
            messages.error(request, 'Há campos obrigatórios em branco!')
            return redirect('escolas_alterar')

        school_data = {
            'cnpj': request.POST['cnpj'], 
            'razao_social': request.POST['corporate-name'], 
            'nome_fantasia': request.POST['trading-name'], 
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
            filename = storage.save(f'escolas/{id}/logos/logo-{id}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            school_data['logo'] = storage.url(filename)
        if 'signature' in request.FILES:
            file = request.FILES['signature']
            storage = MediaStorage()
            filename = storage.save(f'escolas/{id}/assinaturas/assinatura-{id}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            school_data['assinatura'] = storage.url(filename)
        user_data = {
            'first_name': school_data['nome_fantasia'],
            'email': school_data['email'],
        }
        perms_data = {
            'dashboard': 'dashboard' in request.POST,
            'administrativo_escolas': 'administrativo_escolas' in request.POST,
            'administrativo_pessoas_estudantes': 'administrativo_pessoas_estudantes' in request.POST,
            'administrativo_pessoas_responsaveis': 'administrativo_pessoas_responsaveis' in request.POST,
            'administrativo_pessoas_colaboradores': 'administrativo_pessoas_colaboradores' in request.POST,
            'administrativo_contratos': 'administrativo_contratos' in request.POST,
            'administrativo_secretaria': 'administrativo_secretaria' in request.POST,
            'administrativo_recepcao': 'administrativo_recepcao' in request.POST,
            'administrativo_relatorios': 'administrativo_relatorios' in request.POST,
            'pedagogico_cursos': 'pedagogico_cursos' in request.POST,
            'pedagogico_turmas': 'pedagogico_turmas' in request.POST,
            'pedagogico_boletim': 'pedagogico_boletim' in request.POST,
            'pedagogico_diario_classe': 'pedagogico_diario_classe' in request.POST,
            'pedagogico_sala_virtual': 'pedagogico_sala_virtual' in request.POST,
            'pedagogico_vestibulares': 'pedagogico_vestibulares' in request.POST,
            'pedagogico_relatorios': 'pedagogico_relatorios' in request.POST,
            'financeiro_bancos': 'financeiro_bancos' in request.POST,
            'financeiro_movimentacoes': 'financeiro_movimentacoes' in request.POST,
            'financeiro_relatorios': 'financeiro_relatorios' in request.POST,
            'institucional_cadastro_escolar': 'institucional_cadastro_escolar' in request.POST,
            'institucional_usuarios_permissoes': 'institucional_usuarios_permissoes' in request.POST,
            'institucional_ano_academico': 'institucional_ano_academico' in request.POST,
            'institucional_integracoes': 'institucional_integracoes' in request.POST,
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        user_request = requests.patch(f'http://127.0.0.1:8000/api/usuario/{id}/', data=user_data, cookies=cookies, headers=headers)
        school_request = requests.patch(f'http://127.0.0.1:8000/api/escola/{id}/', data=school_data, cookies=cookies, headers=headers)
        perms_request = requests.patch(f'http://127.0.0.1:8000/api/modulos_escola/{id}/', data=perms_data, cookies=cookies, headers=headers)

        return redirect('escolas')


@login_required()
@permission_required('administrativo.delete_escola', raise_exception=True)
def escolas_excluir(request, id):
    school_data = {
        'is_active': False,
    }
    user_data = {
        'is_active': False,
    }
    integration_data = {
        'is_active': False,
    }

    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
    user_request = requests.patch(f'http://127.0.0.1:8000/api/usuario/{id}/', data=user_data, cookies=cookies, headers=headers)
    school_request = requests.patch(f'http://127.0.0.1:8000/api/escola/{id}/', data=school_data, cookies=cookies, headers=headers)
    integration_request = requests.patch(f'http://127.0.0.1:8000/api/integracoes/{id}/', data=integration_data, cookies=cookies, headers=headers)

    return redirect('escolas')



@login_required()
@permission_required('administrativo.view_pessoaestudante', raise_exception=True)
def pessoas_estudantes(request):
    escola = get_school_id(request)
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}

    if 'search' in request.GET:
        search = request.GET['search']
        data = {'estudantes': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/estudantes/?is_active=true&search={search}', cookies=cookies, headers=headers).json()}
    else:
        data = {'estudantes': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/estudantes/?is_active=true', cookies=cookies, headers=headers).json()}

    return render(request, 'administrativo/pessoas_estudantes.html', data)


@login_required()
@permission_required('administrativo.add_pessoaestudante', raise_exception=True)
def pessoas_estudantes_incluir(request):
    if request.method == 'GET':
        return render(request, 'administrativo/pessoas_estudantes_incluir.html')
    if request.method == 'POST':
        if empty_input(request.POST['address-street']) or empty_input(request.POST['address-neighborhood']) or empty_input(request.POST['address-city']) or empty_input(request.POST['address-state']) or empty_input(request.POST['address-country']):
            messages.error(request, 'Há campos obrigatórios em branco!')
            return redirect('pessoas_estudantes_incluir')

        escola = get_school_id(request)
        matricula = request.POST['registration-number']
        if not matricula.strip():
            matricula = f'{str(PessoaEstudante.objects.filter(escola=escola).count()+PessoaColaborador.objects.filter(escola=escola).count()+1).zfill(5)}'

        person_data = {
            'id': str(escola) + str(matricula),
            'escola': escola,
            'matricula': matricula,
            'nome': request.POST['name'],
            'data_nascimento': request.POST['birthdate'],
            'cpf': request.POST['cpf'],
            'rg': request.POST['rg'],
            'celular': request.POST['cellphone-number'],
            'telefone': request.POST['phone-number'],
            'email': request.POST['email'],
            'genero': request.POST['gender'],
            'cor': request.POST['color'],
            'estado_civil': request.POST['marital-status'],
            'cep': request.POST['postal-code'],
            'lougradouro': request.POST['address-street'],
            'numero': request.POST['address-number'],
            'complemento': request.POST['address-complements'],
            'bairro': request.POST['address-neighborhood'],
            'cidade': request.POST['address-city'],
            'estado': request.POST['address-state'],
            'pais': request.POST['address-country'],
            'is_active': True,
        }
        if 'photo' in request.FILES:
            file = request.FILES['photo']
            storage = MediaStorage()
            filename = storage.save(f'pessoas/estudantes/{person_data["id"]}/fotos/foto-{person_data["id"]}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            person_data['foto'] = storage.url(filename)
        user_data = {
            'username': person_data['id'],
            'first_name': person_data['nome'],
            'email': person_data['email'],
            'password': '0',
            'is_active': True,
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        user_request = requests.post('http://127.0.0.1:8000/api/usuario/', data=user_data, cookies=cookies, headers=headers)
        person_data['usuario'] = User.objects.get(username=user_data['username']).id
        person_request = requests.post('http://127.0.0.1:8000/api/pessoas/estudante/', data=person_data, cookies=cookies, headers=headers)

        return redirect('pessoas_estudantes')


@login_required()
@permission_required('administrativo.change_pessoaestudante', raise_exception=True)
def pessoas_estudantes_alterar(request, id):
    if request.method == 'GET':
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        data = {'estudante': requests.get(f'http://127.0.0.1:8000/api/pessoas/estudante/{id}/', cookies=cookies, headers=headers).json()}
        return render(request, 'administrativo/pessoas_estudantes_alterar.html', data)
    if request.method == 'POST':
        if empty_input(request.POST['address-street']) or empty_input(request.POST['address-neighborhood']) or empty_input(request.POST['address-city']) or empty_input(request.POST['address-state']) or empty_input(request.POST['address-country']):
            messages.error(request, 'Há campos obrigatórios em branco!')
            return redirect('pessoas_estudantes_alterar')
        
        person_data = {
            'nome': request.POST['name'],
            'data_nascimento': request.POST['birthdate'],
            'cpf': request.POST['cpf'],
            'rg': request.POST['rg'],
            'celular': request.POST['cellphone-number'],
            'telefone': request.POST['phone-number'],
            'email': request.POST['email'],
            'genero': request.POST['gender'],
            'cor': request.POST['color'],
            'estado_civil': request.POST['marital-status'],
            'cep': request.POST['postal-code'],
            'lougradouro': request.POST['address-street'],
            'numero': request.POST['address-number'],
            'complemento': request.POST['address-complements'],
            'bairro': request.POST['address-neighborhood'],
            'cidade': request.POST['address-city'],
            'estado': request.POST['address-state'],
            'pais': request.POST['address-country'],
        }
        if 'photo' in request.FILES:
            file = request.FILES['photo']
            storage = MediaStorage()
            filename = storage.save(f'pessoas/estudantes/{id}/fotos/foto-{id}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            person_data['foto'] = storage.url(filename)
        user_data = {
            'first_name': person_data['nome'],
            'email': person_data['email'],
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        user_request = requests.patch(f'http://127.0.0.1:8000/api/usuario/{id}/', data=user_data, cookies=cookies, headers=headers)
        person_request = requests.patch(f'http://127.0.0.1:8000/api/pessoas/estudante/{id}/', data=person_data, cookies=cookies, headers=headers)

        ############### CONTA AZUL ###############
        escola = get_school_id(request)
        if IntegracaoContaAzul.objects.filter(escola=escola).exists():
            if IntegracaoContaAzul.objects.get(escola=escola).is_active == True:
                conta_azul_refresh_token = requests.get(f'http://127.0.0.1:8000/institucional/integracoes/conta_azul/refresh_token/', cookies=cookies, headers=headers)
                conta_azul_headers = {'Authorization': f'Bearer {IntegracaoContaAzul.objects.get(escola=escola).access_token}'}
                conta_azul_customer = {
                    'name': person_data['nome'],
                    'email': person_data['email'],
                    'business_phone': person_data['telefone'],
                    'mobile_phone': person_data['celular'],
                    'person_type': 'NATURAL',
                    #'document': person_data['cpf'],
                    #'identity_document': person_data['rg'],
                    'date_of_birth': timezone.make_aware(datetime.combine(datetime.strptime(person_data['data_nascimento'], '%Y-%m-%d'), datetime.min.time())).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                    'address': {
                        'zip_code': person_data['cep'],
                        'street': person_data['lougradouro'],
                        'number': person_data['numero'],
                        'complement': person_data['complemento'],
                        'neighborhood': person_data['bairro'],
                    }
                }
                conta_azul_customer['date_of_birth'] = conta_azul_customer['date_of_birth'][:-8] +conta_azul_customer['date_of_birth'][-5:]
                conta_azul_id = PessoaEstudante.objects.get(pk=id).id_conta_azul
                conta_azul_create_customer_request = requests.put(f'https://api.contaazul.com/v1/customers/{conta_azul_id}/', json=conta_azul_customer, headers=conta_azul_headers)
                try:
                    conta_azul_customer_data = {'id_conta_azul': conta_azul_create_customer_request.json()['id']}
                except:
                    messages.error(request, conta_azul_create_customer_request.content)
                    return redirect('pessoas_estudantes')
                conta_azul_customer_data_request = requests.patch(f'http://127.0.0.1:8000/api/pessoas/estudante/{id}/', data=conta_azul_customer_data, cookies=cookies, headers=headers)

        return redirect('pessoas_estudantes')


@login_required()
@permission_required('administrativo.delete_pessoaestudante', raise_exception=True)
def pessoas_estudantes_excluir(request, id):
    person_data = {
        'is_active': False,
    }
    user_data = {
        'is_active': False,
    }

    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
    user_request = requests.patch(f'http://127.0.0.1:8000/api/usuario/{id}/', data=user_data, cookies=cookies, headers=headers)
    person_request = requests.patch(f'http://127.0.0.1:8000/api/pessoas/estudante/{id}/', data=person_data, cookies=cookies, headers=headers)

    return redirect('pessoas_estudantes')


@login_required()
@permission_required('administrativo.view_pessoaresponsavel', raise_exception=True)
def pessoas_responsaveis(request):
    escola = get_school_id(request)
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}

    if 'search' in request.GET:
        search = request.GET['search']
        data = {'responsaveis': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/responsaveis/?is_active=true&search={search}', cookies=cookies, headers=headers).json()}
    else:
        data = {'responsaveis': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/responsaveis/?is_active=true', cookies=cookies, headers=headers).json()}

    return render(request, 'administrativo/pessoas_responsaveis.html', data)


@login_required()
@permission_required('administrativo.add_pessoaresponsavel', raise_exception=True)
def pessoas_responsaveis_incluir(request):
    if request.method == 'GET':
        return render(request, 'administrativo/pessoas_responsaveis_incluir.html')
    if request.method == 'POST':
        if empty_input(request.POST['address-street']) or empty_input(request.POST['address-neighborhood']) or empty_input(request.POST['address-city']) or empty_input(request.POST['address-state']) or empty_input(request.POST['address-country']):
            messages.error(request, 'Há campos obrigatórios em branco!')
            return redirect('pessoas_responsaveis_incluir')

        escola = get_school_id(request)
        first_student_id = str(request.POST['student-id-0'])
        first_estudante = get_object_or_404(PessoaEstudante, pk=first_student_id)

        person_data = {
            'id': str(first_student_id) + 'r' + str(first_estudante.responsaveis.all().count()+1),
            'escola': escola,
            'estudantes': [],
            'nome': request.POST['name'],
            'data_nascimento': request.POST['birthdate'],
            'cpf': request.POST['cpf'],
            'rg': request.POST['rg'],
            'celular': request.POST['cellphone-number'],
            'telefone': request.POST['phone-number'],
            'email': request.POST['email'],
            'genero': request.POST['gender'],
            'cor': request.POST['color'],
            'estado_civil': request.POST['marital-status'],
            'cep': request.POST['postal-code'],
            'lougradouro': request.POST['address-street'],
            'numero': request.POST['address-number'],
            'complemento': request.POST['address-complements'],
            'bairro': request.POST['address-neighborhood'],
            'cidade': request.POST['address-city'],
            'estado': request.POST['address-state'],
            'pais': request.POST['address-country'],
            'is_active': True,
        }
        if 'photo' in request.FILES:
            file = request.FILES['photo']
            storage = MediaStorage()
            filename = storage.save(f'pessoas/responsaveis/{person_data["id"]}/fotos/foto-{person_data["id"]}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            person_data['foto'] = storage.url(filename)
        user_data = {
            'username': person_data['id'],
            'first_name': person_data['nome'],
            'email': person_data['email'],
            'password': '0',
            'is_active': True,
        }

        i = 0
        while i <= 4:
            try:
                student_id = str(request.POST[f'student-id-{i}'])
                person_data['estudantes'].append(student_id)
                i += 1
            except:
                i += 1

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        user_request = requests.post('http://127.0.0.1:8000/api/usuario/', data=user_data, cookies=cookies, headers=headers)
        person_data['usuario'] = User.objects.get(username=user_data['username']).id
        person_request = requests.post('http://127.0.0.1:8000/api/pessoas/responsavel/', data=person_data, cookies=cookies, headers=headers)

        return redirect('pessoas_responsaveis')


@login_required()
@permission_required('administrativo.change_pessoaresponsavel', raise_exception=True)
def pessoas_responsaveis_alterar(request, id):
    if request.method == 'GET':
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        data = {'responsavel': requests.get(f'http://127.0.0.1:8000/api/pessoas/responsavel/{id}/', cookies=cookies, headers=headers).json()}
        return render(request, 'administrativo/pessoas_responsaveis_alterar.html', data)
    if request.method == 'POST':
        if empty_input(request.POST['address-street']) or empty_input(request.POST['address-neighborhood']) or empty_input(request.POST['address-city']) or empty_input(request.POST['address-state']) or empty_input(request.POST['address-country']):
            messages.error(request, 'Há campos obrigatórios em branco!')
            return redirect('pessoas_responsaveis_alterar')

        person_data = {
            'estudantes': [],
            'nome': request.POST['name'],
            'data_nascimento': request.POST['birthdate'],
            'cpf': request.POST['cpf'],
            'rg': request.POST['rg'],
            'celular': request.POST['cellphone-number'],
            'telefone': request.POST['phone-number'],
            'email': request.POST['email'],
            'genero': request.POST['gender'],
            'cor': request.POST['color'],
            'estado_civil': request.POST['marital-status'],
            'cep': request.POST['postal-code'],
            'lougradouro': request.POST['address-street'],
            'numero': request.POST['address-number'],
            'complemento': request.POST['address-complements'],
            'bairro': request.POST['address-neighborhood'],
            'cidade': request.POST['address-city'],
            'estado': request.POST['address-state'],
            'pais': request.POST['address-country'],
        }
        if 'photo' in request.FILES:
            file = request.FILES['photo']
            storage = MediaStorage()
            filename = storage.save(f'pessoas/responsaveis/{id}/fotos/foto-{id}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            person_data['foto'] = storage.url(filename)
        user_data = {
            'first_name': person_data['nome'],
            'email': person_data['email'],
        }

        i = 0
        while i <= 4:
            try:
                student_id = str(request.POST[f'student-id-{i}'])
                person_data['estudantes'].append(student_id)
                i += 1
            except:
                i += 1

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        user_request = requests.patch(f'http://127.0.0.1:8000/api/usuario/{id}/', data=user_data, cookies=cookies, headers=headers)
        person_request = requests.patch(f'http://127.0.0.1:8000/api/pessoas/responsavel/{id}/', data=person_data, cookies=cookies, headers=headers)

        ############### CONTA AZUL ###############
        escola = get_school_id(request)
        if IntegracaoContaAzul.objects.filter(escola=escola).exists():
            if IntegracaoContaAzul.objects.get(escola=escola).is_active == True:
                conta_azul_refresh_token = requests.get(f'http://127.0.0.1:8000/institucional/integracoes/conta_azul/refresh_token/', cookies=cookies, headers=headers)
                conta_azul_headers = {'Authorization': f'Bearer {IntegracaoContaAzul.objects.get(escola=escola).access_token}'}
                conta_azul_customer = {
                    'name': person_data['nome'],
                    'email': person_data['email'],
                    'business_phone': person_data['telefone'],
                    'mobile_phone': person_data['celular'],
                    'person_type': 'NATURAL',
                    #'document': person_data['cpf'],
                    #'identity_document': person_data['rg'],
                    'date_of_birth': timezone.make_aware(datetime.combine(datetime.strptime(person_data['data_nascimento'], '%Y-%m-%d'), datetime.min.time())).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                    'address': {
                        'zip_code': person_data['cep'],
                        'street': person_data['lougradouro'],
                        'number': person_data['numero'],
                        'complement': person_data['complemento'],
                        'neighborhood': person_data['bairro'],
                    }
                }
                conta_azul_customer['date_of_birth'] = conta_azul_customer['date_of_birth'][:-8] +conta_azul_customer['date_of_birth'][-5:]
                conta_azul_id = PessoaResponsavel.objects.get(pk=id).id_conta_azul
                conta_azul_create_customer_request = requests.put(f'https://api.contaazul.com/v1/customers/{conta_azul_id}/', json=conta_azul_customer, headers=conta_azul_headers)
                try:
                    conta_azul_customer_data = {'id_conta_azul': conta_azul_create_customer_request.json()['id']}
                except:
                    messages.error(request, conta_azul_create_customer_request.content)
                    return redirect('pessoas_responsaveis')
                conta_azul_customer_data_request = requests.patch(f'http://127.0.0.1:8000/api/pessoas/responsavel/{id}/', data=conta_azul_customer_data, cookies=cookies, headers=headers)

        return redirect('pessoas_responsaveis')


@login_required()
@permission_required('administrativo.delete_pessoaresponsavel', raise_exception=True)
def pessoas_responsaveis_excluir(request, id):
    person_data = {
        'is_active': False,
    }
    user_data = {
        'is_active': False,
    }

    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
    user_request = requests.patch(f'http://127.0.0.1:8000/api/usuario/{id}/', data=user_data, cookies=cookies, headers=headers)
    person_request = requests.patch(f'http://127.0.0.1:8000/api/pessoas/responsavel/{id}/', data=person_data, cookies=cookies, headers=headers)

    return redirect('pessoas_responsaveis')


@login_required()
@permission_required('administrativo.view_pessoacolaborador', raise_exception=True)
def pessoas_colaboradores(request):
    escola = get_school_id(request)
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}

    if 'search' in request.GET:
        search = request.GET['search']
        data = {'colaboradores': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/colaboradores/?is_active=true&search={search}', cookies=cookies, headers=headers).json()}
    else:
        data = {'colaboradores': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/colaboradores/?is_active=true', cookies=cookies, headers=headers).json()}

    return render(request, 'administrativo/pessoas_colaboradores.html', data)


@login_required()
@permission_required('administrativo.add_pessoacolaborador', raise_exception=True)
def pessoas_colaboradores_incluir(request):
    if request.method == 'GET':
        return render(request, 'administrativo/pessoas_colaboradores_incluir.html')
    if request.method == 'POST':
        if empty_input(request.POST['address-street']) or empty_input(request.POST['address-neighborhood']) or empty_input(request.POST['address-city']) or empty_input(request.POST['address-state']) or empty_input(request.POST['address-country']):
            messages.error(request, 'Há campos obrigatórios em branco!')
            return redirect('pessoas_colaboradores_incluir')

        escola = get_school_id(request)
        matricula = request.POST['registration-number']
        if not matricula.strip():
            matricula = f'{str(PessoaEstudante.objects.filter(escola=escola).count()+PessoaColaborador.objects.filter(escola=escola).count()+1).zfill(5)}'
        if request.POST['firing-date']:
            demissao = request.POST['firing-date']
        else:
            demissao = None

        person_data = {
            'id': str(escola) + str(matricula),
            'escola': escola,
            'matricula': matricula,
            'nome': request.POST['name'],
            'data_nascimento': request.POST['birthdate'],
            'cpf': request.POST['cpf'],
            'rg': request.POST['rg'],
            'celular': request.POST['cellphone-number'],
            'telefone': request.POST['phone-number'],
            'email': request.POST['email'],
            'genero': request.POST['gender'],
            'cor': request.POST['color'],
            'estado_civil': request.POST['marital-status'],
            'cep': request.POST['postal-code'],
            'lougradouro': request.POST['address-street'],
            'numero': request.POST['address-number'],
            'complemento': request.POST['address-complements'],
            'bairro': request.POST['address-neighborhood'],
            'cidade': request.POST['address-city'],
            'estado': request.POST['address-state'],
            'pais': request.POST['address-country'],
            'departamento': request.POST['department'],
            'cargo': request.POST['position'],
            'ramal': request.POST['extension'],
            'admissao': request.POST['hiring-date'],
            'demissao': demissao,
            'remuneracao': request.POST['salary'],
            'banco': request.POST['bank'],
            'agencia': request.POST['bank-branch'],
            'conta': request.POST['bank-account'],
            'is_active': True,
        }
        if 'photo' in request.FILES:
            file = request.FILES['photo']
            storage = MediaStorage()
            filename = storage.save(f'pessoas/colaboradores/{person_data["id"]}/fotos/foto-{person_data["id"]}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            person_data['foto'] = storage.url(filename)
        user_data = {
            'username': person_data['id'],
            'first_name': person_data['nome'],
            'email': person_data['email'],
            'password': '0',
            'is_active': True,
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        user_request = requests.post('http://127.0.0.1:8000/api/usuario/', data=user_data, cookies=cookies, headers=headers)
        person_data['usuario'] = User.objects.get(username=user_data['username']).id
        person_request = requests.post('http://127.0.0.1:8000/api/pessoas/colaborador/', data=person_data, cookies=cookies, headers=headers)

        return redirect('pessoas_colaboradores')


@login_required()
@permission_required('administrativo.change_pessoacolaborador', raise_exception=True)
def pessoas_colaboradores_alterar(request, id):
    if request.method == 'GET':
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        data = {'colaborador': requests.get(f'http://127.0.0.1:8000/api/pessoas/colaborador/{id}/', cookies=cookies, headers=headers).json()}
        return render(request, 'administrativo/pessoas_colaboradores_alterar.html', data)
    if request.method == 'POST':
        if empty_input(request.POST['address-street']) or empty_input(request.POST['address-neighborhood']) or empty_input(request.POST['address-city']) or empty_input(request.POST['address-state']) or empty_input(request.POST['address-country']):
            messages.error(request, 'Há campos obrigatórios em branco!')
            return redirect('pessoas_colaboradores_alterar')

        if request.POST['firing-date']:
            demissao = request.POST['firing-date']
        else:
            demissao = None

        person_data = {
            'nome': request.POST['name'],
            'data_nascimento': request.POST['birthdate'],
            'cpf': request.POST['cpf'],
            'rg': request.POST['rg'],
            'celular': request.POST['cellphone-number'],
            'telefone': request.POST['phone-number'],
            'email': request.POST['email'],
            'genero': request.POST['gender'],
            'cor': request.POST['color'],
            'estado_civil': request.POST['marital-status'],
            'cep': request.POST['postal-code'],
            'lougradouro': request.POST['address-street'],
            'numero': request.POST['address-number'],
            'complemento': request.POST['address-complements'],
            'bairro': request.POST['address-neighborhood'],
            'cidade': request.POST['address-city'],
            'estado': request.POST['address-state'],
            'pais': request.POST['address-country'],
            'departamento': request.POST['department'],
            'cargo': request.POST['position'],
            'ramal': request.POST['extension'],
            'admissao': request.POST['hiring-date'],
            'demissao': demissao,
            'remuneracao': request.POST['salary'],
            'banco': request.POST['bank'],
            'agencia': request.POST['bank-branch'],
            'conta': request.POST['bank-account'],
        }
        if 'photo' in request.FILES:
            file = request.FILES['photo']
            storage = MediaStorage()
            filename = storage.save(f'pessoas/colaboradores/{id}/fotos/foto-{id}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            person_data['foto'] = storage.url(filename)
        user_data = {
            'first_name': person_data['nome'],
            'email': person_data['email'],
        }

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        user_request = requests.patch(f'http://127.0.0.1:8000/api/usuario/{id}/', data=user_data, cookies=cookies, headers=headers)
        person_request = requests.patch(f'http://127.0.0.1:8000/api/pessoas/colaborador/{id}/', data=person_data, cookies=cookies, headers=headers)

        return redirect('pessoas_colaboradores')


@login_required()
@permission_required('administrativo.delete_pessoacolaborador', raise_exception=True)
def pessoas_colaboradores_excluir(request, id):
    person_data = {
        'is_active': False,
    }
    user_data = {
        'is_active': False,
    }

    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
    user_request = requests.patch(f'http://127.0.0.1:8000/api/usuario/{id}/', data=user_data, cookies=cookies, headers=headers)
    person_request = requests.patch(f'http://127.0.0.1:8000/api/pessoas/colaborador/{id}/', data=person_data, cookies=cookies, headers=headers)

    return redirect('pessoas_colaboradores')



@login_required()
@permission_required('administrativo.view_contratoeducacional', raise_exception=True)
def contratos(request):
    escola = get_school_id(request)
    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}

    if 'search' in request.GET:
        search = request.GET['search']
        data = {'contratos': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/contratos_educacionais/?deleted=false&search={search}', cookies=cookies, headers=headers).json()}
    else:
        data = {'contratos': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/contratos_educacionais/?deleted=false', cookies=cookies, headers=headers).json()}

    for item in data['contratos']:
        item['data_assinatura'] = parse_date(item['data_assinatura'])
        item['estudante'] = ContratoEducacional.objects.get(pk=item['id']).estudante
        item['curso'] = ContratoEducacional.objects.get(pk=item['id']).curso
        item['turma'] = ContratoEducacional.objects.get(pk=item['id']).turma
    return render(request, 'administrativo/contratos.html', data)


@login_required()
@permission_required('administrativo.add_contratoeducacional', raise_exception=True)
def contratos_incluir(request):
    if request.method == 'GET':
        escola = get_school_id(request)
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        data = {'cursos': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/cursos/?is_active=true', cookies=cookies, headers=headers).json()}
        return render(request, 'administrativo/contratos_incluir.html', data)
    elif request.method == 'POST':
        if request.POST['type'] == 'Educacional':
            escola = Escola.objects.get(pk=get_school_id(request))
            estudante_contratante = 'is-student-contractor' in request.POST
            curso = Curso.objects.get(pk=request.POST['course-id'])
            turma = Turma.objects.get(pk=request.POST['class-id'])
            estudante = PessoaEstudante.objects.get(pk=request.POST['student-id'])
            if estudante_contratante is False:
                responsavel = PessoaResponsavel.objects.get(pk=request.POST['guardian-id'])

            extenso = dExtenso()
            inicio_pagamento = datetime(int(request.POST['payment-start'].split('-')[0]), int(request.POST['payment-start'].split('-')[1]), int(request.POST['payment-start'].split('-')[2]))
            data_assinatura = datetime(int(request.POST['sign-date'].split('-')[0]), int(request.POST['sign-date'].split('-')[1]), int(request.POST['sign-date'].split('-')[2]))

            if estudante_contratante is True:
                contratante = estudante
                tipo_pessoa = 'estudante'
            elif estudante_contratante is False:
                contratante = responsavel
                tipo_pessoa = 'responsavel'
            if request.POST['contract-code']:
                codigo_contrato = request.POST['contract-code']
                id_contrato = str(escola.id) + codigo_contrato
            else:
                codigo_contrato = str(ContratoEducacional.objects.filter(escola=escola.id).count() + 1).zfill(6)
                id_contrato = str(escola.id) + codigo_contrato

            variaveis_dict = {
                'contratante_nome': contratante.nome,
                'contratante_rg': contratante.rg,
                'contratante_cpf': contratante.cpf,
                'contratante_endereco_lougradouro': contratante.lougradouro,
                'contratante_endereco_numero': contratante.numero,
                'contratante_endereco_complemento': contratante.complemento,
                'contratante_endereco_bairro': contratante.bairro,
                'contratante_endereco_cidade': contratante.cidade,
                'contratante_endereco_estado': contratante.estado,
                'contratante_endereco_cep': contratante.cep,
                'curso_descricao': curso.descricao,
                'data_inicio': turma.data_inicio.strftime('%d/%m/%Y'),
                'data_termino': turma.data_termino.strftime('%d/%m/%Y'),
                'custo_total_curso': turma.valor_curso,
                'custo_total_curso_extenso': extenso.getExtenso(int(float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))) + ' reais e ' + extenso.getExtenso(int(100*round(float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.'))-int(float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.'))), 2))) + ' centavos',
                'parcelas_totais_curso': turma.parcelamento_curso,
                'custo_total_parcelas_curso': 'R$ ' + locale.format('%.2f', round(float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.'))/int(turma.parcelamento_curso), 2), grouping=True),
                'custo_total_parcelas_curso_extenso': extenso.getExtenso(int(float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.'))/int(turma.parcelamento_curso))) + ' reais e ' + extenso.getExtenso(int(100*round(float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.'))/int(turma.parcelamento_curso)-int(float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.'))/int(turma.parcelamento_curso)), 2))) + ' centavos',
                'percentual_desconto_curso': request.POST['discount'],
                'custo_final_curso': 'R$ ' + locale.format('%.2f', round((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')), 2), grouping=True),
                'custo_final_curso_extenso': extenso.getExtenso(int((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))) + ' reais e ' + extenso.getExtenso(int(100*round((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.'))-int(int((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))), 2))) + ' centavos',
                'parcelas_finais_curso': request.POST['installments'],
                'custo_final_parcelas_curso': 'R$ ' + locale.format('%.2f', round(((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))/int(request.POST['installments']), 2), grouping=True),
                'custo_final_parcelas_curso_extenso': extenso.getExtenso(int(float(((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))/int(request.POST['installments'])))) + ' reais e ' + extenso.getExtenso(int(100*round(float(((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))/int(request.POST['installments']))-int(float(((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))/int(request.POST['installments']))), 2))) + ' centavos',
                'dia_pagamento': request.POST['payment-day'],
                'mes_inicio_pagamento': inicio_pagamento.strftime('%B'),
                'ano_inicio_pagamento': inicio_pagamento.year,
                'custo_total_material': turma.valor_material,
                'custo_total_material_extenso': extenso.getExtenso(int(float(turma.valor_material.replace('R$ ', '').replace('.', '').replace(',', '.')))) + ' reais e ' + extenso.getExtenso(int(100*round(float(turma.valor_material.replace('R$ ', '').replace('.', '').replace(',', '.'))-int(float(turma.valor_material.replace('R$ ', '').replace('.', '').replace(',', '.'))), 2))) + ' centavos',
                'parcelas_totais_material': turma.parcelamento_material,
                'data_assinatura': f'{data_assinatura.day} de {data_assinatura.strftime("%B")} de {data_assinatura.year}',
                'escola_nome_fantasia': escola.nome_fantasia,
                'escola_cnpj': escola.cnpj,
            }
            if estudante_contratante is False:
                variaveis_dict['estudante_nome'] = estudante.nome
                variaveis_dict['estudante_rg'] = estudante.rg
                variaveis_dict['estudante_cpf'] = estudante.cpf

            file = contrato_educacional(request, variaveis_dict, estudante_contratante)
            storage = MediaStorage()
            filename = storage.save(f'contratos/educacionais/{escola.id}/arquivos/contrato-{id_contrato}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            contract_file_url = storage.url(filename)

            contract_data = {
                'id': id_contrato,
                'codigo': codigo_contrato,
                'escola': escola.id,
                'curso': curso.id,
                'turma': turma.id,
                'data_assinatura': data_assinatura.strftime("%Y-%m-%d"),
                'estudante': estudante.id,
                'estudante_contratante': estudante_contratante,
                'desconto_pagamento_matricula': request.POST['registration-discount'],
                'data_pagamento_matricula': request.POST['registration-payment-date'],
                'desconto_pagamento_curso': variaveis_dict['percentual_desconto_curso'],
                'parcelas_pagamento_curso': variaveis_dict['parcelas_finais_curso'],
                'dia_pagamento_curso': variaveis_dict['dia_pagamento'],
                'data_inicio_pagamento_curso': inicio_pagamento.strftime("%Y-%m-%d"),
                'arquivo_contrato': contract_file_url,
                'deleted': False,
            }
            if contract_data['estudante_contratante'] is False:
                contract_data['responsavel'] = responsavel.id

            cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
            headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
            contract_request = requests.post('http://127.0.0.1:8000/api/contrato_educacional/', data=contract_data, cookies=cookies, headers=headers)

            ############### CONTA AZUL ###############
            if IntegracaoContaAzul.objects.filter(escola=escola.id).exists():
                if IntegracaoContaAzul.objects.get(escola=escola.id).is_active == True:
                    conta_azul_refresh_token = requests.get(f'http://127.0.0.1:8000/institucional/integracoes/conta_azul/refresh_token/', cookies=cookies, headers=headers)
                    conta_azul_headers = {'Authorization': f'Bearer {IntegracaoContaAzul.objects.get(escola=escola.id).access_token}'}
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
                    conta_azul_customer['date_of_birth'] = conta_azul_customer['date_of_birth'][:-8] +conta_azul_customer['date_of_birth'][-5:]
                    try:
                        conta_azul_create_customer_request = requests.post(f'https://api.contaazul.com/v1/customers/', json=conta_azul_customer, headers=conta_azul_headers)
                        conta_azul_customer_data = {'id_conta_azul': conta_azul_create_customer_request.json()['id']}
                        conta_azul_customer_data_request = requests.patch(f'http://127.0.0.1:8000/api/pessoas/{tipo_pessoa}/{contratante.id}/', data=conta_azul_customer_data, cookies=cookies, headers=headers)
                    except:
                        pass


                    conta_azul_contract = {
                        'number': int(contract_data['codigo']),
                        'emission': timezone.make_aware(datetime.combine(datetime.strptime(contract_data['data_inicio_pagamento_curso'], '%Y-%m-%d'), datetime.min.time())).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                        'status': 'COMMITTED',
                        'customer_id': contratante.id_conta_azul,
                        'services': [
                            {
                                'quantity': 1,
                                'service_id': Turma.objects.get(pk=contract_data['turma']).id_conta_azul,
                                'value': round(float(float((Turma.objects.get(pk=contract_data['turma']).valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))*(1-(float(contract_data['desconto_pagamento_curso'].replace('%', '').replace(',', '.'))/100))/int(contract_data['parcelas_pagamento_curso'])),2) + float(3.50*int(contract_data['parcelas_pagamento_curso'])),
                            },
                        ],
                        #'discount': {
                        #  'measure_unit': 'PERCENT',
                        #  'rate': float(contract_data['desconto_pagamento_curso'].replace('%', '').replace(',', '.')),
                        #},
                        'due_day': int(contract_data['dia_pagamento_curso']),
                        'duration': int(contract_data['parcelas_pagamento_curso']),
                    }
                    conta_azul_contract['emission'] = conta_azul_contract['emission'][:-8] + conta_azul_contract['emission'][-5:]
                    conta_azul_create_contract_request = requests.post(f'https://api.contaazul.com/v1/contracts/', json=conta_azul_contract, headers=conta_azul_headers)
                    try:
                        conta_azul_contract_data = {'id_conta_azul': conta_azul_create_contract_request.json()['id']}
                    except:
                        messages.error(request, conta_azul_create_contract_request.content)
                        return redirect('contratos')
                    conta_azul_contract_data_request = requests.patch(f'http://127.0.0.1:8000/api/contrato_educacional/{contract_data["id"]}/', data=conta_azul_contract_data, cookies=cookies, headers=headers)

            return redirect('contratos')


@login_required()
@permission_required('administrativo.change_contratoeducacional', raise_exception=True)
def contratos_digitalizar(request, id):
    if request.method == 'GET':
        escola = get_school_id(request)
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        data = {'contrato': requests.get(f'http://127.0.0.1:8000/api/contrato_educacional/{id}/', cookies=cookies, headers=headers).json(), 'cursos': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/cursos/?is_active=true', cookies=cookies, headers=headers).json()}
        return render(request, 'administrativo/contratos_digitalizar.html', data)
    if request.method == 'POST':
        escola = Escola.objects.get(pk=get_school_id(request))
        contract_data = {}
        if 'digitalized-copy' in request.FILES:
            file = request.FILES['digitalized-copy']
            storage = MediaStorage()
            filename = storage.save(f'contratos/educacionais/{escola.id}/digitalizacoes/digitalizacao-contrato-{id}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            contract_data['digitalizacao'] = storage.url(filename)

        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        contract_request = requests.patch(f'http://127.0.0.1:8000/api/contrato_educacional/{id}/', data=contract_data, cookies=cookies, headers=headers)

        return redirect('contratos')


@login_required()
@permission_required('administrativo.change_contratoeducacional', raise_exception=True)
def contratos_alterar(request, id):
    if request.method == 'GET':
        escola = get_school_id(request)
        cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
        data = {'contrato': requests.get(f'http://127.0.0.1:8000/api/contrato_educacional/{id}/', cookies=cookies, headers=headers).json(), 'cursos': requests.get(f'http://127.0.0.1:8000/api/escola/{escola}/cursos/?is_active=true', cookies=cookies, headers=headers).json()}
        return render(request, 'administrativo/contratos_alterar.html', data)
    elif request.method == 'POST':
        if request.POST['type'] == 'Educacional':
            escola = Escola.objects.get(pk=get_school_id(request))
            estudante_contratante = 'is-student-contractor' in request.POST
            curso = Curso.objects.get(pk=request.POST['course-id'])
            turma = Turma.objects.get(pk=request.POST['class-id'])
            estudante = PessoaEstudante.objects.get(pk=request.POST['student-id'])
            if estudante_contratante is False:
                responsavel = PessoaResponsavel.objects.get(pk=request.POST['guardian-id'])

            extenso = dExtenso()
            inicio_pagamento = datetime(int(request.POST['payment-start'].split('-')[0]), int(request.POST['payment-start'].split('-')[1]), int(request.POST['payment-start'].split('-')[2]))
            data_assinatura = datetime(int(request.POST['sign-date'].split('-')[0]), int(request.POST['sign-date'].split('-')[1]), int(request.POST['sign-date'].split('-')[2]))

            if estudante_contratante is True:
                contratante = estudante
                tipo_pessoa = 'estudante'
            elif estudante_contratante is False:
                contratante = responsavel
                tipo_pessoa = 'responsavel'

            variaveis_dict = {
                'contratante_nome': contratante.nome,
                'contratante_rg': contratante.rg,
                'contratante_cpf': contratante.cpf,
                'contratante_endereco_lougradouro': contratante.lougradouro,
                'contratante_endereco_numero': contratante.numero,
                'contratante_endereco_complemento': contratante.complemento,
                'contratante_endereco_bairro': contratante.bairro,
                'contratante_endereco_cidade': contratante.cidade,
                'contratante_endereco_estado': contratante.estado,
                'contratante_endereco_cep': contratante.cep,
                'curso_descricao': curso.descricao,
                'data_inicio': turma.data_inicio.strftime('%d/%m/%Y'),
                'data_termino': turma.data_termino.strftime('%d/%m/%Y'),
                'custo_total_curso': turma.valor_curso,
                'custo_total_curso_extenso': extenso.getExtenso(int(float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))) + ' reais e ' + extenso.getExtenso(int(100*round(float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.'))-int(float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.'))), 2))) + ' centavos',
                'parcelas_totais_curso': turma.parcelamento_curso,
                'custo_total_parcelas_curso': 'R$ ' + locale.format('%.2f', round(float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.'))/int(turma.parcelamento_curso), 2), grouping=True),
                'custo_total_parcelas_curso_extenso': extenso.getExtenso(int(float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.'))/int(turma.parcelamento_curso))) + ' reais e ' + extenso.getExtenso(int(100*round(float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.'))/int(turma.parcelamento_curso)-int(float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.'))/int(turma.parcelamento_curso)), 2))) + ' centavos',
                'percentual_desconto_curso': request.POST['discount'],
                'custo_final_curso': 'R$ ' + locale.format('%.2f', round((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')), 2), grouping=True),
                'custo_final_curso_extenso': extenso.getExtenso(int((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))) + ' reais e ' + extenso.getExtenso(int(100*round((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.'))-int(int((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))), 2))) + ' centavos',
                'parcelas_finais_curso': request.POST['installments'],
                'custo_final_parcelas_curso': 'R$ ' + locale.format('%.2f', round(((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))/int(request.POST['installments']), 2), grouping=True),
                'custo_final_parcelas_curso_extenso': extenso.getExtenso(int(float(((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))/int(request.POST['installments'])))) + ' reais e ' + extenso.getExtenso(int(100*round(float(((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))/int(request.POST['installments']))-int(float(((1 - (float(request.POST['discount'].replace(',', '.').replace('%', ''))/100)) * float(turma.valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))/int(request.POST['installments']))), 2))) + ' centavos',
                'dia_pagamento': request.POST['payment-day'],
                'mes_inicio_pagamento': inicio_pagamento.strftime('%B'),
                'ano_inicio_pagamento': inicio_pagamento.year,
                'custo_total_material': turma.valor_material,
                'custo_total_material_extenso': extenso.getExtenso(int(float(turma.valor_material.replace('R$ ', '').replace('.', '').replace(',', '.')))) + ' reais e ' + extenso.getExtenso(int(100*round(float(turma.valor_material.replace('R$ ', '').replace('.', '').replace(',', '.'))-int(float(turma.valor_material.replace('R$ ', '').replace('.', '').replace(',', '.'))), 2))) + ' centavos',
                'parcelas_totais_material': turma.parcelamento_material,
                'data_assinatura': f'{data_assinatura.day} de {data_assinatura.strftime("%B")} de {data_assinatura.year}',
                'escola_nome_fantasia': escola.nome_fantasia,
                'escola_cnpj': escola.cnpj,
            }
            if estudante_contratante is False:
                variaveis_dict['estudante_nome'] = estudante.nome
                variaveis_dict['estudante_rg'] = estudante.rg
                variaveis_dict['estudante_cpf'] = estudante.cpf

            file = contrato_educacional(request, variaveis_dict, estudante_contratante)
            storage = MediaStorage()
            filename = storage.save(f'contratos/educacionais/{escola.id}/arquivos/contrato-{id}-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}', file)
            contract_file_url = storage.url(filename)

            contract_data = {
                'escola': escola.id,
                'curso': curso.id,
                'turma': turma.id,
                'data_assinatura': data_assinatura.strftime("%Y-%m-%d"),
                'estudante': estudante.id,
                'estudante_contratante': estudante_contratante,
                'desconto_pagamento_matricula': request.POST['registration-discount'],
                'data_pagamento_matricula': request.POST['registration-payment-date'],
                'desconto_pagamento_curso': variaveis_dict['percentual_desconto_curso'],
                'parcelas_pagamento_curso': variaveis_dict['parcelas_finais_curso'],
                'dia_pagamento_curso': variaveis_dict['dia_pagamento'],
                'data_inicio_pagamento_curso': inicio_pagamento.strftime("%Y-%m-%d"),
                'arquivo_contrato': contract_file_url,
                'deleted': False,
            }
            if contract_data['estudante_contratante'] is False:
                contract_data['responsavel'] = responsavel.id

            cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
            headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
            contract_request = requests.patch(f'http://127.0.0.1:8000/api/contrato_educacional/{id}/', data=contract_data, cookies=cookies, headers=headers)

            ############### CONTA AZUL ###############
            if IntegracaoContaAzul.objects.filter(escola=escola.id).exists():
                if IntegracaoContaAzul.objects.get(escola=escola.id).is_active == True:
                    conta_azul_refresh_token = requests.get(f'http://127.0.0.1:8000/institucional/integracoes/conta_azul/refresh_token/', cookies=cookies, headers=headers)
                    conta_azul_headers = {'Authorization': f'Bearer {IntegracaoContaAzul.objects.get(escola=escola.id).access_token}'}
                    """try:
                        conta_azul_customer = {
                            'name': contratante.nome,
                            'email': contratante.email,
                            'business_phone': contratante.telefone,
                            'mobile_phone': contratante.celular,
                            'person_type': 'NATURAL',
                            'document': contratante.cpf,
                            'identity_document': contratante.rg,
                            'date_of_birth': timezone.make_aware(datetime.combine(datetime.strptime(contratante.data_nascimento, '%Y-%m-%d'), datetime.min.time())).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
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
                        pass"""

                    conta_azul_refresh_token = requests.get(f'http://127.0.0.1:8000/institucional/integracoes/conta_azul/refresh_token/', cookies=cookies, headers=headers)
                    conta_azul_contract = {
                        'number': int(str(id)[-6:]),
                        'emission': timezone.make_aware(datetime.combine(datetime.strptime(contract_data['data_inicio_pagamento_curso'], '%Y-%m-%d'), datetime.min.time())).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                        'status': 'COMMITTED',
                        'customer_id': contratante.id_conta_azul,
                        'services': [
                            {
                                'quantity': 1,
                                'service_id': Turma.objects.get(pk=contract_data['turma']).id_conta_azul,
                                'value': round(float(float((Turma.objects.get(pk=contract_data['turma']).valor_curso.replace('R$ ', '').replace('.', '').replace(',', '.')))*(1-(float(contract_data['desconto_pagamento_curso'].replace('%', '').replace(',', '.'))/100))/int(contract_data['parcelas_pagamento_curso'])),2) + float(3.50*int(contract_data['parcelas_pagamento_curso'])),
                            },
                        ],
                        #'discount': {
                        #  'measure_unit': 'PERCENT',
                        #  'rate': float(contract_data['desconto_pagamento_curso'].replace('%', '').replace(',', '.')),
                        #},
                        'due_day': int(contract_data['dia_pagamento_curso']),
                        'duration': int(contract_data['parcelas_pagamento_curso']),
                    }
                    conta_azul_contract['emission'] = conta_azul_contract['emission'][:-8] + conta_azul_contract['emission'][-5:]
                    conta_azul_create_contract_request = requests.post(f'https://api.contaazul.com/v1/contracts/', json=conta_azul_contract, headers=conta_azul_headers)
                    try:
                        conta_azul_contract_data = {'id_conta_azul': conta_azul_create_contract_request.json()['id']}
                    except:
                        messages.error(request, conta_azul_create_contract_request.content)
                        return redirect('contratos')
                    conta_azul_contract_data_request = requests.patch(f'http://127.0.0.1:8000/api/contrato_educacional/{id}/', data=conta_azul_contract_data, cookies=cookies, headers=headers)

            return redirect('contratos')


@login_required()
@permission_required('administrativo.delete_contratoeducacional', raise_exception=True)
def contratos_excluir(request, id):
    contract_data = {
        'deleted': True,
    }

    cookies = {'csrftoken': request.COOKIES['csrftoken'], 'sessionid': request.session.session_key}
    headers = {'X-CSRFToken': cookies['csrftoken'], 'Referer': 'http://127.0.0.1:8000'}
    contract_request = requests.patch(f'http://127.0.0.1:8000/api/contrato_educacional/{id}/', data=contract_data, cookies=cookies, headers=headers)

    return redirect('contratos')



@login_required()
def secretaria(request):
    return render(request, 'administrativo/secretaria.html')



@login_required()
def recepcao(request):
    return render(request, 'administrativo/recepcao.html')



@login_required()
def administrativo_relatorios(request):
    return render(request, 'administrativo/relatorios.html')
