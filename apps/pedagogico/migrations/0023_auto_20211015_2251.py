# Generated by Django 3.2.7 on 2021-10-16 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0026_auto_20211015_2251'),
        ('pedagogico', '0022_auto_20211015_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='disciplinas',
            field=models.ManyToManyField(blank=True, related_name='cursos', to='pedagogico.Disciplina'),
        ),
        migrations.AlterField(
            model_name='turma',
            name='alunos',
            field=models.ManyToManyField(blank=True, related_name='turmas', to='administrativo.PessoaEstudante'),
        ),
    ]
