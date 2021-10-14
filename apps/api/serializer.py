import requests, json
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from administrativo.models import Escola, ModulosEscola, ContratoEducacional, ContratoTrabalhista, PessoaEstudante, PessoaResponsavel, PessoaColaborador
from pedagogico.models import Disciplina, Curso, Turma
from institucional.models import AnoAcademico, UsuariosPermissoes
from funcionalidades.models import Email

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        lookup_field = 'username'
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            email = validated_data['email'],
            is_active = validated_data['is_active'],
        )
        user.set_password(User.objects.make_random_password())
        user.save()

        email_data = {
            'tipo': 'NOVO_USUARIO',
            'remetente_nome': self.context['request'].user.escola.nome_fantasia,
            'remetente_email': self.context['request'].user.escola.email,
            'destinatarios': [validated_data['email']],
            'assunto': 'Bem-vindo(a) à Athena!',
            'variaveis': json.dumps({
                'nome': validated_data['first_name'],
                'escola': self.context['request'].user.escola.nome_fantasia,
            }, indent=4),
        }
        cookies = {'csrftoken': self.context['request'].COOKIES['csrftoken'], 'sessionid': self.context['request'].session.session_key}
        headers = {'X-CSRFToken': cookies['csrftoken']}
        email_request = requests.post('http://127.0.0.1:8000/api/email/', data=email_data, cookies=cookies, headers=headers)

        return user

class GruposUsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = '__all__'

class ModulosEscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModulosEscola
        fields = '__all__'
        lookup_field = 'escola'

class ContratoEducacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoEducacional
        fields = '__all__'

class ContratoTrabalhistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoTrabalhista
        fields = '__all__'

class PessoaEstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PessoaEstudante
        fields = '__all__'

class PessoaResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PessoaResponsavel
        fields = '__all__'

class PessoaColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PessoaColaborador
        fields = '__all__'

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'

class AnoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnoAcademico
        fields = '__all__'

class UsuariosPermissoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuariosPermissoes
        fields = '__all__'

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'
