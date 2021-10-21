from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User

def empty_input(input):
    return not input.strip()



def login(request):
    if request.method == 'GET':
        return render(request, 'usuario/login.html')
    elif request.method == 'POST':
        usuario = request.POST['username']
        senha = request.POST['password']

        if empty_input(usuario) or empty_input(senha):
            messages.error(request, 'Há campos obrigatórios em branco!')
            return redirect('login')

        if User.objects.filter(username=usuario).exists():
            user = auth.authenticate(request, username=usuario, password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Senha inválida!')
                return redirect('login')
        else:
            messages.error(request, 'Usuário não cadastrado!')
            return redirect('login')


@login_required()
def logout(request):
    auth.logout(request)
    return redirect('login')


def signup(request):
    return render(request, 'usuario/signup.html')


@login_required()
def perfil(request):
    return render(request, 'usuario/perfil.html')


@login_required()
def preferencias(request):
    return render(request, 'usuario/preferencias.html')
