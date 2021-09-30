from django.shortcuts import render, redirect

def index(request):
    return redirect('dashboard')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'index/dashboard.html')
    else:
        return redirect('login')        
