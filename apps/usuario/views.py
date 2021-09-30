from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User

def empty_input(input):
    if not input.strip():
        return redirect('login')



def login(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        senha = request.POST['password']

        empty_input(usuario)
        empty_input(senha)

        if User.objects.filter(username=usuario).exists():
            user = auth.authenticate(request, username=usuario, password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
        return redirect('signup')
    else:
        return render(request, 'usuario/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def signup(request):
    return render(request, 'usuario/signup.html')

def perfil(request):
    return render(request, 'usuario/perfil.html')

def preferencias(request):
    return render(request, 'usuario/preferencias.html')
