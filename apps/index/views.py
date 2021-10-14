from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def index(request):
    return redirect('dashboard')

@login_required()
def dashboard(request):
        return render(request, 'index/dashboard.html')
