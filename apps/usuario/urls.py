from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('usuario/perfil/', views.perfil, name='perfil'),
    path('usuario/preferencias/', views.preferencias, name='preferencias'),
]
