# Generated by Django 3.2.7 on 2021-10-04 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrativo', '0013_auto_20211003_2102'),
        ('institucional', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=6)),
                ('descricao', models.CharField(max_length=100)),
                ('divisao_periodos', models.CharField(max_length=100)),
                ('proposta_pedagogica', models.FileField(blank=True, upload_to='disciplinas/ementas/%Y')),
                ('horarios', models.FileField(blank=True, upload_to='disciplinas/horarios/%Y')),
                ('valor_curso', models.IntegerField(blank=True)),
                ('parcelamento_curso', models.IntegerField(blank=True)),
                ('valor_material', models.IntegerField(blank=True)),
                ('parcelamento_material', models.IntegerField(blank=True)),
                ('data_final_cancelamento', models.DateField(blank=True, null=True)),
                ('coordenador', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='administrativo.pessoacolaborador')),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=6)),
                ('descricao', models.CharField(max_length=100)),
                ('turno', models.CharField(max_length=50)),
                ('alunos', models.ManyToManyField(blank=True, related_name='turma', to='administrativo.PessoaEstudante')),
                ('ano_academico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institucional.anoacademico')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedagogico.curso')),
                ('tutor', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='administrativo.pessoacolaborador')),
            ],
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=6)),
                ('descricao', models.CharField(max_length=100)),
                ('divisao_periodos', models.CharField(max_length=100)),
                ('ementa', models.FileField(blank=True, upload_to='disciplinas/ementas/%Y')),
                ('horarios', models.FileField(blank=True, upload_to='disciplinas/horarios/%Y')),
                ('coordenador', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='disciplina_coordenador', to='administrativo.pessoacolaborador')),
                ('professores', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='disciplina_professores', to='administrativo.pessoacolaborador')),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='disciplinas',
            field=models.ManyToManyField(related_name='curso', to='pedagogico.Disciplina'),
        ),
    ]
