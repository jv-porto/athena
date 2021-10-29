from django.urls import path, include
from rest_framework import routers
from .views import UsuarioViewSet, GruposUsuariosViewSet, EscolaViewSet, ContratoEducacionalViewSet, ContratoTrabalhistaViewSet, PessoaEstudanteViewSet, PessoaResponsavelViewSet, PessoaColaboradorViewSet, DisciplinaViewSet, CursoViewSet, TurmaViewSet, AnoAcademicoViewSet, UsuariosPermissoesViewSet, ModulosEscolaViewSet, EmailViewSet, IntegracoesViewSet, IntegracaoContaAzulViewSet
from .views import EscolaUsuarios, EscolaContratosEducacionais, EscolaContratosTrabalhistas, EscolaEstudantes, EscolaResponsaveis, EscolaColaboradores, EscolaDisciplinas, EscolaCursos, EscolaTurmas, CursoTurmas, EscolaAnosAcademicos, EscolaUsuariosPermissoes

router = routers.DefaultRouter()
router.register('usuario', UsuarioViewSet, basename='api-usuario')
router.register('grupos_usuarios', GruposUsuariosViewSet, basename='api-grupos-usuarios')
router.register('escola', EscolaViewSet, basename='api-escola')
router.register('modulos_escola', ModulosEscolaViewSet, basename='api-modulos-escola')
router.register('contrato_educacional', ContratoEducacionalViewSet, basename='api-contrato-educacional')
router.register('contrato_trabalhista', ContratoTrabalhistaViewSet, basename='api-contrato-trabalhista')
router.register('pessoas/estudante', PessoaEstudanteViewSet, basename='api-pessoa-estudante')
router.register('pessoas/responsavel', PessoaResponsavelViewSet, basename='api-pessoa-responsavel')
router.register('pessoas/colaborador', PessoaColaboradorViewSet, basename='api-pessoa-colaborador')
router.register('disciplina', DisciplinaViewSet, basename='api-disciplina')
router.register('curso', CursoViewSet, basename='api-curso')
router.register('turma', TurmaViewSet, basename='api-turma')
router.register('ano_academico', AnoAcademicoViewSet, basename='api-ano-academico')
router.register('usuarios_permissoes', UsuariosPermissoesViewSet, basename='api-usuarios-permissoes')
router.register('email', EmailViewSet, basename='api-email')
router.register('integracoes', IntegracoesViewSet, basename='api-integracoes')
router.register('integracao_conta_azul', IntegracaoContaAzulViewSet, basename='api-integracao-conta-azul')

urlpatterns = [
    path('', include(router.urls)),
    path('escola/<str:school_id>/usuarios/', EscolaUsuarios.as_view()),
    path('escola/<str:school_id>/contratos_educacionais/', EscolaContratosEducacionais.as_view()),
    path('escola/<str:school_id>/contratos_trabalhistas/', EscolaContratosTrabalhistas.as_view()),
    path('escola/<str:school_id>/estudantes/', EscolaEstudantes.as_view()),
    path('escola/<str:school_id>/responsaveis/', EscolaResponsaveis.as_view()),
    path('escola/<str:school_id>/colaboradores/', EscolaColaboradores.as_view()),
    path('escola/<str:school_id>/disciplinas/', EscolaDisciplinas.as_view()),
    path('escola/<str:school_id>/cursos/', EscolaCursos.as_view()),
    path('escola/<str:school_id>/turmas/', EscolaTurmas.as_view()),
    path('curso/<str:course_id>/turmas/', CursoTurmas.as_view()),
    path('escola/<str:school_id>/anos_academicos/', EscolaAnosAcademicos.as_view()),
    path('escola/<str:school_id>/usuarios_permissoes/', EscolaUsuariosPermissoes.as_view()),
]
