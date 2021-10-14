from django.urls import path
from . import views

urlpatterns = [
    path('calendario/', views.calendario, name='calendario'),
    path('mensagens/', views.mensagens, name='mensagens'),
    path('mensagens/email/', views.email, name='email'),
]
