# Generated by Django 3.2.7 on 2021-10-13 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0022_auto_20211012_2243'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContratoEducacional',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('valor', models.CharField(max_length=20)),
                ('arquivo', models.CharField(max_length=200)),
                ('digitalizacao', models.CharField(blank=True, max_length=200, null=True)),
                ('data_assinatura', models.DateField()),
                ('datahora_ultima_alteracao', models.DateTimeField(auto_now=True)),
                ('datahora_cadastro', models.DateTimeField(auto_now_add=True)),
                ('escola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrativo.escola')),
            ],
        ),
        migrations.CreateModel(
            name='ContratoTrabalhista',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('valor', models.CharField(max_length=20)),
                ('arquivo', models.CharField(max_length=200)),
                ('digitalizacao', models.CharField(blank=True, max_length=200, null=True)),
                ('data_assinatura', models.DateField()),
                ('datahora_ultima_alteracao', models.DateTimeField(auto_now=True)),
                ('datahora_cadastro', models.DateTimeField(auto_now_add=True)),
                ('escola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrativo.escola')),
            ],
        ),
        migrations.RemoveField(
            model_name='pessoacolaborador',
            name='contratos',
        ),
        migrations.RemoveField(
            model_name='pessoaestudante',
            name='contratos',
        ),
        migrations.RemoveField(
            model_name='pessoaresponsavel',
            name='contratos',
        ),
        migrations.DeleteModel(
            name='Contrato',
        ),
    ]