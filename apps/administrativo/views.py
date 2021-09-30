from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Escola, PessoaEstudante, PessoaResponsavel, PessoaColaborador, Contrato

def empty_input(input):
    if not input.strip():
        return redirect('escolas_incluir')

def different_passwords(password, password_confirmation):
    if password != password_confirmation:
        return redirect('escolas_incluir')





def escolas(request):
    if request.user.is_authenticated:
        escolas = Escola.objects.filter(is_active=True).order_by('datahora_cadastro')
        data = {'escolas': escolas}
        return render(request, 'administrativo/escolas.html', data)
    else:
        return redirect('login')

def escolas_incluir(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            escola_id = f'{str(Escola.objects.all().count()+1).zfill(4)}'
            cnpj = request.POST['cnpj']
            razao_social = request.POST['corporate-name']
            nome_fantasia = request.POST['trading-name']
            email = request.POST['email']
            telefone = request.POST['phone-number']
            celular = request.POST['cellphone-number']
            site = request.POST['website']
            cep = request.POST['postal-code']
            lougradouro = request.POST['address-street']
            numero = request.POST['address-number']
            complemento = request.POST['address-complements']
            bairro = request.POST['address-neighborhood']
            cidade = request.POST['address-city']
            estado = request.POST['address-state']
            pais = request.POST['address-country']
            usuario = f'{str(Escola.objects.all().count()+1).zfill(4)}'
            senha = request.POST['password']
            senha_confirmacao = request.POST['password-confirmation']

            empty_input(razao_social)
            empty_input(nome_fantasia)
            empty_input(lougradouro)
            empty_input(bairro)
            empty_input(cidade)
            empty_input(estado)
            empty_input(pais)
            empty_input(usuario)
            different_passwords(senha, senha_confirmacao)

            user = User.objects.create_user(first_name=nome_fantasia, username=usuario, email=email, password=senha)
            user.save()
            escola = Escola.objects.create(id=escola_id, cnpj=cnpj, razao_social=razao_social, nome_fantasia=nome_fantasia, email=email, telefone=telefone, celular=celular, site=site, cep=cep, lougradouro=lougradouro, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, estado=estado, pais=pais, usuario=user)
            escola.save()
            return redirect('escolas')
        else:
            return render(request, 'administrativo/escolas_incluir.html')
    else:
        return redirect('login')

def escolas_alterar_page(request, id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            escola = get_object_or_404(Escola, pk=id)
            edicao = {'escola': escola}
            return render(request, 'administrativo/escolas_alterar.html', edicao)
    else:
        return redirect('login')

def escolas_alterar(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            empty_input(request.POST['corporate-name'])
            empty_input(request.POST['trading-name'])
            empty_input(request.POST['address-street'])
            empty_input(request.POST['address-neighborhood'])
            empty_input(request.POST['address-city'])
            empty_input(request.POST['address-state'])
            empty_input(request.POST['address-country'])

            escola_id = request.POST['school-code']
            escola = Escola.objects.get(pk=escola_id)
            escola.cnpj = request.POST['cnpj']
            escola.razao_social = request.POST['corporate-name']
            escola.nome_fantasia = request.POST['trading-name']
            escola.email = request.POST['email']
            escola.telefone = request.POST['phone-number']
            escola.celular = request.POST['cellphone-number']
            escola.site = request.POST['website']
            escola.cep = request.POST['postal-code']
            escola.lougradouro = request.POST['address-street']
            escola.numero = request.POST['address-number']
            escola.complemento = request.POST['address-complements']
            escola.bairro = request.POST['address-neighborhood']
            escola.cidade = request.POST['address-city']
            escola.estado = request.POST['address-state']
            escola.pais = request.POST['address-country']
            senha = request.POST['password']
            senha_confirmacao = request.POST['password-confirmation']
            if senha == senha_confirmacao:
                escola.usuario.set_password(senha)
            else:
                return redirect('escolas_alterar_page', escola_id)

            escola.save()
            escola.usuario.save()
            return redirect('escolas')
    else:
        return redirect('login')

def escolas_excluir(request, id):
    if request.user.is_authenticated:
        escola = get_object_or_404(Escola, pk=id)
        usuario = User.objects.get(username=escola.usuario)
        usuario.is_active = False
        escola.is_active = False
        usuario.save()
        escola.save()
        return redirect('escolas')
    else:
        return redirect('login')





def pessoas_estudantes(request):
    if request.user.is_authenticated:
        pessoas = PessoaEstudante.objects.filter(is_active=True).order_by('datahora_cadastro')
        data = {'pessoas': pessoas}
        return render(request, 'administrativo/pessoas_estudantes.html', data)
    else:
        return redirect('login')

def pessoas_responsaveis(request):
    if request.user.is_authenticated:
        pessoas = PessoaResponsavel.objects.filter(is_active=True).order_by('datahora_cadastro')
        data = {'pessoas': pessoas}
        return render(request, 'administrativo/pessoas_responsaveis.html', data)
    else:
        return redirect('login')

def pessoas_colaboradores(request):
    if request.user.is_authenticated:
        pessoas = PessoaColaborador.objects.filter(is_active=True).order_by('datahora_cadastro')
        data = {'pessoas': pessoas}
        return render(request, 'administrativo/pessoas_colaboradores.html', data)
    else:
        return redirect('login')

def find_estudante(request, id):
    if request.user.is_authenticated:
        found_pessoa = get_object_or_404(PessoaEstudante, pk=id)
        data = {
            'id': found_pessoa.id,
            'escola_id': found_pessoa.escola.id,
            'matricula': found_pessoa.matricula,
            'nome': found_pessoa.nome,
            'data_nascimento': found_pessoa.data_nascimento,
            'usuario_username': found_pessoa.usuario.username,
            'datahora_ultima_alteracao': found_pessoa.datahora_ultima_alteracao,
            'datahora_cadastro': found_pessoa.datahora_cadastro,
            'is_active': found_pessoa.is_active,
        }
        return JsonResponse(data)

def pessoas_estudantes_incluir(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            escola = request.user.escola
            escola_id = escola.id
            matricula = request.POST['registration-number']
            if not matricula.strip():
                matricula = f'{str(PessoaEstudante.objects.all().count()+PessoaColaborador.objects.all().count()+1).zfill(5)}'
            id = str(escola_id) + str(matricula)
            nome = request.POST['name']
            data_nascimento = request.POST['birthdate']
            cpf = request.POST['cpf']
            rg = request.POST['rg']
            celular = request.POST['cellphone-number']
            telefone = request.POST['phone-number']
            email = request.POST['email']
            genero = request.POST['gender']
            cor = request.POST['color']
            estado_civil = request.POST['marital-status']
            foto = request.POST['photo']
            cep = request.POST['postal-code']
            lougradouro = request.POST['address-street']
            numero = request.POST['address-number']
            complemento = request.POST['address-complements']
            bairro = request.POST['address-neighborhood']
            cidade = request.POST['address-city']
            estado = request.POST['address-state']
            pais = request.POST['address-country']
            usuario = id
            senha = request.POST['password']
            senha_confirmacao = request.POST['password-confirmation']

            empty_input(nome)
            empty_input(lougradouro)
            empty_input(bairro)
            empty_input(cidade)
            empty_input(estado)
            empty_input(pais)
            different_passwords(senha, senha_confirmacao)

            user = User.objects.create_user(first_name=nome, username=usuario, email=email, password=senha)
            user.save()
            estudante = PessoaEstudante.objects.create(id=id, escola=escola, matricula=matricula, nome=nome, data_nascimento=data_nascimento, cpf=cpf, rg=rg, celular=celular, telefone=telefone, email=email, genero=genero, cor=cor, estado_civil=estado_civil, foto=foto, cep=cep, lougradouro=lougradouro, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, estado=estado, pais=pais, usuario=user)
            estudante.save()
            return redirect('pessoas_estudantes')
        else:
            return render(request, 'administrativo/pessoas_estudantes_incluir.html')
    else:
        return redirect('login')

def pessoas_responsaveis_incluir(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            first_student_id = str(request.POST['student-id-0'])
            first_estudante = get_object_or_404(PessoaEstudante, pk=first_student_id)
            id = str(first_student_id) + 'r' + str(first_estudante.responsavel.all().count()+1)
            escola = request.user.escola
            nome = request.POST['name']
            data_nascimento = request.POST['birthdate']
            cpf = request.POST['cpf']
            rg = request.POST['rg']
            celular = request.POST['cellphone-number']
            telefone = request.POST['phone-number']
            email = request.POST['email']
            genero = request.POST['gender']
            cor = request.POST['color']
            estado_civil = request.POST['marital-status']
            foto = request.POST['photo']
            cep = request.POST['postal-code']
            lougradouro = request.POST['address-street']
            numero = request.POST['address-number']
            complemento = request.POST['address-complements']
            bairro = request.POST['address-neighborhood']
            cidade = request.POST['address-city']
            estado = request.POST['address-state']
            pais = request.POST['address-country']
            usuario = id
            senha = request.POST['password']
            senha_confirmacao = request.POST['password-confirmation']

            empty_input(nome)
            empty_input(lougradouro)
            empty_input(bairro)
            empty_input(cidade)
            empty_input(estado)
            empty_input(pais)
            different_passwords(senha, senha_confirmacao)

            user = User.objects.create_user(first_name=nome, username=usuario, email=email, password=senha)
            user.save()
            responsavel = PessoaResponsavel.objects.create(id=id, escola=escola, nome=nome, data_nascimento=data_nascimento, cpf=cpf, rg=rg, celular=celular, telefone=telefone, email=email, genero=genero, cor=cor, estado_civil=estado_civil, foto=foto, cep=cep, lougradouro=lougradouro, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, estado=estado, pais=pais, usuario=user)
            responsavel.save()

            i = 0
            while i <= 4:
                try:
                    student_id = str(request.POST[f'student-id-{i}'])
                    estudante = get_object_or_404(PessoaEstudante, pk=student_id)
                    responsavel.estudantes.add(estudante)
                    responsavel.save()
                    i += 1
                except:
                    i += 1
            return redirect('pessoas_responsaveis')
        else:
            return render(request, 'administrativo/pessoas_responsaveis_incluir.html')
    else:
        return redirect('login')

def pessoas_colaboradores_incluir(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            escola = request.user.escola
            escola_id = escola.id
            matricula = request.POST['registration-number']
            if not matricula.strip():
                matricula = f'{str(PessoaEstudante.objects.all().count()+PessoaColaborador.objects.all().count()+1).zfill(5)}'
            id = str(escola_id) + str(matricula)
            nome = request.POST['name']
            data_nascimento = request.POST['birthdate']
            cpf = request.POST['cpf']
            rg = request.POST['rg']
            celular = request.POST['cellphone-number']
            telefone = request.POST['phone-number']
            email = request.POST['email']
            genero = request.POST['gender']
            cor = request.POST['color']
            estado_civil = request.POST['marital-status']
            foto = request.POST['photo']
            cep = request.POST['postal-code']
            lougradouro = request.POST['address-street']
            numero = request.POST['address-number']
            complemento = request.POST['address-complements']
            bairro = request.POST['address-neighborhood']
            cidade = request.POST['address-city']
            estado = request.POST['address-state']
            pais = request.POST['address-country']
            departamento = request.POST['department']
            cargo = request.POST['position']
            ramal = request.POST['extension']
            admissao = request.POST['hiring-date']
            if request.POST['firing-date']:
                demissao = request.POST['firing-date']
            else:
                demissao = None
            remuneracao = request.POST['salary']
            banco = request.POST['bank']
            agencia = request.POST['bank-branch']
            conta = request.POST['bank-account']
            usuario = id
            senha = request.POST['password']
            senha_confirmacao = request.POST['password-confirmation']

            empty_input(nome)
            empty_input(lougradouro)
            empty_input(bairro)
            empty_input(cidade)
            empty_input(estado)
            empty_input(pais)
            different_passwords(senha, senha_confirmacao)

            user = User.objects.create_user(first_name=nome, username=usuario, email=email, password=senha)
            user.save()
            colaborador = PessoaColaborador.objects.create(id=id, escola=escola, matricula=matricula, nome=nome, data_nascimento=data_nascimento, cpf=cpf, rg=rg, celular=celular, telefone=telefone, email=email, genero=genero, cor=cor, estado_civil=estado_civil, foto=foto, cep=cep, lougradouro=lougradouro, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, estado=estado, pais=pais, departamento=departamento, cargo=cargo, ramal=ramal, admissao=admissao, demissao=demissao, remuneracao=remuneracao, banco=banco, agencia=agencia, conta=conta, usuario=user)
            colaborador.save()
            return redirect('pessoas_colaboradores')
        else:
            return render(request, 'administrativo/pessoas_colaboradores_incluir.html')
    else:
        return redirect('login')

def pessoas_estudantes_alterar_page(request, id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            estudante = get_object_or_404(PessoaEstudante, pk=id)
            edicao = {'estudante': estudante}
            return render(request, 'administrativo/pessoas_estudantes_alterar.html', edicao)
    else:
        return redirect('login')

def pessoas_estudantes_alterar(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            empty_input(request.POST['name'])
            empty_input(request.POST['address-street'])
            empty_input(request.POST['address-neighborhood'])
            empty_input(request.POST['address-city'])
            empty_input(request.POST['address-state'])
            empty_input(request.POST['address-country'])

            id = request.POST['student-id']
            estudante = PessoaEstudante.objects.get(pk=id)
            estudante.nome = request.POST['name']
            estudante.data_nascimento = request.POST['birthdate']
            estudante.cpf = request.POST['cpf']
            estudante.rg = request.POST['rg']
            estudante.celular = request.POST['cellphone-number']
            estudante.telefone = request.POST['phone-number']
            estudante.email = request.POST['email']
            """estudante.genero = request.POST['gender']
            estudante.cor = request.POST['color']
            estudante.estado_civil = request.POST['marital-status']"""
            if 'foto' in request.FILES:
                estudante.foto = request.FILES['photo']
            estudante.cep = request.POST['postal-code']
            estudante.lougradouro = request.POST['address-street']
            estudante.numero = request.POST['address-number']
            estudante.complemento = request.POST['address-complements']
            estudante.bairro = request.POST['address-neighborhood']
            estudante.cidade = request.POST['address-city']
            estudante.estado = request.POST['address-state']
            estudante.pais = request.POST['address-country']
            senha = request.POST['password']
            senha_confirmacao = request.POST['password-confirmation']
            if senha == senha_confirmacao:
                estudante.usuario.set_password(senha)
            else:
                return redirect('pessoas_estudantes_alterar_page', id)

            estudante.save()
            estudante.usuario.save()
            return redirect('pessoas_estudantes')
    else:
        return redirect('login')

def pessoas_responsaveis_alterar_page(request, id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            responsavel = get_object_or_404(PessoaResponsavel, pk=id)
            edicao = {'responsavel': responsavel}
            return render(request, 'administrativo/pessoas_responsaveis_alterar.html', edicao)
    else:
        return redirect('login')

def pessoas_responsaveis_alterar(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            empty_input(request.POST['name'])
            empty_input(request.POST['address-street'])
            empty_input(request.POST['address-neighborhood'])
            empty_input(request.POST['address-city'])
            empty_input(request.POST['address-state'])
            empty_input(request.POST['address-country'])

            id = request.POST['id']
            responsavel = PessoaResponsavel.objects.get(pk=id)
            responsavel.nome = request.POST['name']
            responsavel.data_nascimento = request.POST['birthdate']
            responsavel.cpf = request.POST['cpf']
            responsavel.rg = request.POST['rg']
            responsavel.celular = request.POST['cellphone-number']
            responsavel.telefone = request.POST['phone-number']
            responsavel.email = request.POST['email']
            """responsavel.genero = request.POST['gender']
            responsavel.cor = request.POST['color']
            responsavel.estado_civil = request.POST['marital-status']"""
            if 'foto' in request.FILES:
                responsavel.foto = request.FILES['photo']
            responsavel.cep = request.POST['postal-code']
            responsavel.lougradouro = request.POST['address-street']
            responsavel.numero = request.POST['address-number']
            responsavel.complemento = request.POST['address-complements']
            responsavel.bairro = request.POST['address-neighborhood']
            responsavel.cidade = request.POST['address-city']
            responsavel.estado = request.POST['address-state']
            responsavel.pais = request.POST['address-country']
            #estudantes
            senha = request.POST['password']
            senha_confirmacao = request.POST['password-confirmation']
            if senha == senha_confirmacao:
                responsavel.usuario.set_password(senha)
            else:
                return redirect('pessoas_responsaveis_alterar_page', id)

            responsavel.save()
            responsavel.usuario.save()
            return redirect('pessoas_responsaveis')
    else:
        return redirect('login')

def pessoas_colaboradores_alterar_page(request, id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            colaborador = get_object_or_404(PessoaColaborador, pk=id)
            edicao = {'colaborador': colaborador}
            return render(request, 'administrativo/pessoas_colaboradores_alterar.html', edicao)
    else:
        return redirect('login')

def pessoas_colaboradores_alterar(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            empty_input(request.POST['name'])
            empty_input(request.POST['address-street'])
            empty_input(request.POST['address-neighborhood'])
            empty_input(request.POST['address-city'])
            empty_input(request.POST['address-state'])
            empty_input(request.POST['address-country'])

            id = request.POST['id']
            colaborador = PessoaColaborador.objects.get(pk=id)
            colaborador.nome = request.POST['name']
            colaborador.data_nascimento = request.POST['birthdate']
            colaborador.cpf = request.POST['cpf']
            colaborador.rg = request.POST['rg']
            colaborador.celular = request.POST['cellphone-number']
            colaborador.telefone = request.POST['phone-number']
            colaborador.email = request.POST['email']
            """colaborador.genero = request.POST['gender']
            colaborador.cor = request.POST['color']
            colaborador.estado_civil = request.POST['marital-status']"""
            if 'foto' in request.FILES:
                colaborador.foto = request.FILES['photo']
            colaborador.cep = request.POST['postal-code']
            colaborador.lougradouro = request.POST['address-street']
            colaborador.numero = request.POST['address-number']
            colaborador.complemento = request.POST['address-complements']
            colaborador.bairro = request.POST['address-neighborhood']
            colaborador.cidade = request.POST['address-city']
            colaborador.estado = request.POST['address-state']
            colaborador.pais = request.POST['address-country']
            colaborador.departamento = request.POST['department']
            colaborador.cargo = request.POST['position']
            colaborador.ramal = request.POST['extension']
            colaborador.admissao = request.POST['hiring-date']
            colaborador.demissao = request.POST['firing-date']
            colaborador.remuneracao = request.POST['salary']
            colaborador.banco = request.POST['bank']
            colaborador.agencia = request.POST['bank-branch']
            colaborador.conta = request.POST['bank-account']
            senha = request.POST['password']
            senha_confirmacao = request.POST['password-confirmation']
            if senha == senha_confirmacao:
                colaborador.usuario.set_password(senha)
            else:
                return redirect('pessoas_colaboradores_alterar_page', id)

            colaborador.save()
            colaborador.usuario.save()
            return redirect('pessoas_colaboradores')
    else:
        return redirect('login')

def pessoas_estudantes_excluir(request, id):
    if request.user.is_authenticated:
        estudante = get_object_or_404(PessoaEstudante, pk=id)
        usuario = User.objects.get(username=estudante.usuario)
        usuario.is_active = False
        estudante.is_active = False
        usuario.save()
        estudante.save()
        return redirect('pessoas_estudantes')
    else:
        return redirect('login')

def pessoas_responsaveis_excluir(request, id):
    if request.user.is_authenticated:
        responsavel = get_object_or_404(PessoaResponsavel, pk=id)
        usuario = User.objects.get(username=responsavel.usuario)
        usuario.is_active = False
        responsavel.is_active = False
        usuario.save()
        responsavel.save()
        return redirect('pessoas_responsaveis')
    else:
        return redirect('login')

def pessoas_colaboradores_excluir(request, id):
    if request.user.is_authenticated:
        colaborador = get_object_or_404(PessoaColaborador, pk=id)
        usuario = User.objects.get(username=colaborador.usuario)
        usuario.is_active = False
        colaborador.is_active = False
        usuario.save()
        colaborador.save()
        return redirect('pessoas_colaboradores')
    else:
        return redirect('login')





def contratos(request):
    if request.user.is_authenticated:
        contratos = Contrato.objects.filter(is_active=True).order_by('datahora_cadastro')
        data = {'contratos': contratos}
        return render(request, 'administrativo/contratos.html', data)
    else:
        return redirect('login')

def contratos_incluir(request):
    if request.user.is_authenticated:
        return render(request, 'administrativo/contratos_incluir.html')
    else:
        return redirect('login')

def secretaria(request):
    if request.user.is_authenticated:
        return render(request, 'administrativo/secretaria.html')
    else:
        return redirect('login')

def recepcao(request):
    if request.user.is_authenticated:
        return render(request, 'administrativo/recepcao.html')
    else:
        return redirect('login')

def administrativo_relatorios(request):
    if request.user.is_authenticated:
        return render(request, 'administrativo/relatorios.html')
    else:
        return redirect('login')
