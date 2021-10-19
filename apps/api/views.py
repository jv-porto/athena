from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters
from django.contrib.auth.models import User, Group
from administrativo.models import Escola, ModulosEscola, ContratoEducacional, ContratoTrabalhista, PessoaEstudante, PessoaResponsavel, PessoaColaborador
from pedagogico.models import Disciplina, Curso, Turma
from institucional.models import AnoAcademico, UsuariosPermissoes
from funcionalidades.models import Email
from .serializer import UsuarioSerializer, GruposUsuariosSerializer, EscolaSerializer, ContratoEducacionalSerializer, ContratoTrabalhistaSerializer, PessoaEstudanteSerializer, PessoaResponsavelSerializer, PessoaColaboradorSerializer, DisciplinaSerializer, CursoSerializer, TurmaSerializer, AnoAcademicoSerializer, UsuariosPermissoesSerializer, ModulosEscolaSerializer, EmailSerializer

############### VIEWSETS ###############
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UsuarioSerializer
    lookup_field = 'username'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']

class GruposUsuariosViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GruposUsuariosSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class EscolaViewSet(viewsets.ModelViewSet):
    queryset = Escola.objects.all().order_by('id')
    serializer_class = EscolaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id', 'cnpj', 'razao_social', 'nome_fantasia', 'email', 'telefone', 'celular']
    filterset_fields = ['is_active']

class ModulosEscolaViewSet(viewsets.ModelViewSet):
    queryset = ModulosEscola.objects.all().order_by('escola')
    serializer_class = ModulosEscolaSerializer
    lookup_field = 'escola'
    filter_backends = [filters.SearchFilter]
    search_fields = ['escola', 'descricao']

class ContratoEducacionalViewSet(viewsets.ModelViewSet):
    queryset = ContratoEducacional.objects.all().order_by('id')
    serializer_class = ContratoEducacionalSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['id', 'tipo', 'data_assinatura']
    filterset_fields = ['deleted']

class ContratoTrabalhistaViewSet(viewsets.ModelViewSet):
    queryset = ContratoTrabalhista.objects.all().order_by('id')
    serializer_class = ContratoTrabalhistaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['id', 'tipo', 'data_assinatura']
    filterset_fields = ['deleted']

class PessoaEstudanteViewSet(viewsets.ModelViewSet):
    queryset = PessoaEstudante.objects.all().order_by('id')
    serializer_class = PessoaEstudanteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id', 'escola', 'nome', 'data_nascimento', 'cpf', 'rg', 'celular', 'telefone', 'email', 'contratos']
    filterset_fields = ['is_active']

class PessoaResponsavelViewSet(viewsets.ModelViewSet):
    queryset = PessoaResponsavel.objects.all().order_by('id')
    serializer_class = PessoaResponsavelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id', 'escola', 'estudantes', 'nome', 'data_nascimento', 'cpf', 'rg', 'celular', 'telefone', 'email', 'contratos']
    filterset_fields = ['is_active']

class PessoaColaboradorViewSet(viewsets.ModelViewSet):
    queryset = PessoaColaborador.objects.all().order_by('id')
    serializer_class = PessoaColaboradorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id', 'escola', 'nome', 'data_nascimento', 'cpf', 'rg', 'celular', 'telefone', 'email', 'departamento', 'cargo', 'ramal', 'contratos']
    filterset_fields = ['is_active']

class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all().order_by('id')
    serializer_class = DisciplinaSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']
    search_fields = ['id', 'descricao', 'divisao_periodos', 'coordenador', 'professores']

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all().order_by('id')
    serializer_class = CursoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']
    search_fields = ['id', 'descricao', 'divisao_periodos', 'coordenador', 'disciplinas', 'data_final_cancelamento']
    filterset_fields = ['is_active']

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all().order_by('id')
    serializer_class = TurmaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']
    search_fields = ['id', 'descricao', 'ano_academico', 'curso', 'turno', 'tutor', 'alunos']
    filterset_fields = ['deleted']

class AnoAcademicoViewSet(viewsets.ModelViewSet):
    queryset = AnoAcademico.objects.all().order_by('id')
    serializer_class = AnoAcademicoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'descricao', 'periodicidade']

class UsuariosPermissoesViewSet(viewsets.ModelViewSet):
    queryset = UsuariosPermissoes.objects.all().order_by('escola')
    serializer_class = UsuariosPermissoesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['escola', 'descricao']

class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all().order_by('tipo')
    serializer_class = EmailSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['tipo']





############### API VIEW ###############
########## ESCOLAS ##########
class EscolaUsuarios(generics.ListAPIView):
    def get_queryset(self):
        queryset = User.objects.filter(escola=self.kwargs['school_id'])
        return queryset
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']

class EscolaContratosEducacionais(generics.ListAPIView):
    def get_queryset(self):
        queryset = ContratoEducacional.objects.filter(escola=self.kwargs['school_id'])
        return queryset
    serializer_class = ContratoEducacionalSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id', 'razao_social', 'nome_fantasia', 'email', 'telefone', 'celular']
    filterset_fields = ['deleted']

class EscolaContratosTrabalhistas(generics.ListAPIView):
    def get_queryset(self):
        queryset = ContratoTrabalhista.objects.filter(escola=self.kwargs['school_id'])
        return queryset
    serializer_class = ContratoTrabalhistaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id', 'razao_social', 'nome_fantasia', 'email', 'telefone', 'celular']
    filterset_fields = ['deleted']

class EscolaEstudantes(generics.ListAPIView):
    def get_queryset(self):
        queryset = PessoaEstudante.objects.filter(escola=self.kwargs['school_id'])
        return queryset
    serializer_class = PessoaEstudanteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id', 'nome', 'data_nascimento', 'cpf', 'rg', 'celular', 'telefone', 'email', 'contratos']
    filterset_fields = ['is_active']

class EscolaResponsaveis(generics.ListAPIView):
    def get_queryset(self):
        queryset = PessoaResponsavel.objects.filter(escola=self.kwargs['school_id'])
        return queryset
    serializer_class = PessoaResponsavelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id', 'estudantes', 'nome', 'data_nascimento', 'cpf', 'rg', 'celular', 'telefone', 'email', 'contratos']
    filterset_fields = ['is_active']

class EscolaColaboradores(generics.ListAPIView):
    def get_queryset(self):
        queryset = PessoaColaborador.objects.filter(escola=self.kwargs['school_id'])
        return queryset
    serializer_class = PessoaColaboradorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id', 'nome', 'data_nascimento', 'cpf', 'rg', 'celular', 'telefone', 'email', 'departamento', 'cargo', 'ramal', 'contratos']
    filterset_fields = ['is_active']

class EscolaDisciplinas(generics.ListAPIView):
    def get_queryset(self):
        queryset = Disciplina.objects.filter(escola=self.kwargs['school_id'])
        return queryset
    serializer_class = DisciplinaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id', 'descricao', 'divisao_periodos', 'coordenador', 'professores']

class EscolaCursos(generics.ListAPIView):
    def get_queryset(self):
        queryset = Curso.objects.filter(escola=self.kwargs['school_id'])
        return queryset
    serializer_class = CursoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    rdering_fields = ['id']
    search_fields = ['id', 'descricao', 'divisao_periodos', 'coordenador', 'disciplinas', 'data_final_cancelamento']
    filterset_fields = ['is_active']

class EscolaTurmas(generics.ListAPIView):
    def get_queryset(self):
        queryset = Turma.objects.filter(escola=self.kwargs['school_id'])
        return queryset
    serializer_class = TurmaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']
    search_fields = ['id', 'descricao', 'ano_academico', 'curso', 'turno', 'tutor', 'alunos']
    filterset_fields = ['deleted']

class CursoTurmas(generics.ListAPIView):
    def get_queryset(self):
        queryset = Turma.objects.filter(curso=self.kwargs['course_id'])
        return queryset
    serializer_class = TurmaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']
    search_fields = ['id', 'descricao', 'ano_academico', 'curso', 'turno', 'tutor', 'alunos']
    filterset_fields = ['deleted']

class EscolaAnosAcademicos(generics.ListAPIView):
    def get_queryset(self):
        queryset = AnoAcademico.objects.filter(escola=self.kwargs['school_id'])
        return queryset
    serializer_class = AnoAcademicoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id', 'descricao', 'periodicidade']
    filterset_fields = ['deleted']

class EscolaUsuariosPermissoes(generics.ListAPIView):
    def get_queryset(self):
        queryset = UsuariosPermissoes.objects.filter(escola=self.kwargs['school_id'])
        return queryset
    serializer_class = UsuariosPermissoesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['escola', 'descricao']
    filterset_fields = ['is_active']
