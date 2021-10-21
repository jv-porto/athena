from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),

    path('usuario/perfil/', views.perfil, name='perfil'),
    path('usuario/preferencias/', views.preferencias, name='preferencias'),

    path('senha/alterar/', auth_views.PasswordChangeView.as_view(template_name='usuario/alterar_senha.html'), name='password_change'),
    path('senha/alterar/sucesso/', auth_views.PasswordChangeDoneView.as_view(template_name='usuario/alterar_senha_sucesso.html'), name='password_change_done'),

    path('senha/esqueci/', auth_views.PasswordResetView.as_view(template_name='usuario/esqueci_senha.html'), name='password_reset'),
    path('senha/esqueci/sucesso/', auth_views.PasswordResetDoneView.as_view(template_name='usuario/esqueci_senha_sucesso.html'), name='password_reset_done'),

    path('senha/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='usuario/redefinir_senha.html'), name='password_reset_confirm'),
    path('senha/reset/sucesso/', auth_views.PasswordResetCompleteView.as_view(template_name='usuario/redefinir_senha_sucesso.html'), name='password_reset_complete'),
]
