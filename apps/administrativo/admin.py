from django.contrib import admin
from .models import Escola, PessoaEstudante, PessoaResponsavel, PessoaColaborador

admin.site.register(Escola)
admin.site.register(PessoaEstudante)
admin.site.register(PessoaResponsavel)
admin.site.register(PessoaColaborador)
