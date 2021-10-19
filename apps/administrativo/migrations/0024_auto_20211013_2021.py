# Generated by Django 3.2.7 on 2021-10-13 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0023_auto_20211013_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoacolaborador',
            name='contratos',
            field=models.ManyToManyField(blank=True, related_name='colaborador', to='administrativo.ContratoTrabalhista'),
        ),
        migrations.AddField(
            model_name='pessoaestudante',
            name='contratos',
            field=models.ManyToManyField(blank=True, related_name='estudante', to='administrativo.ContratoEducacional'),
        ),
        migrations.AddField(
            model_name='pessoaresponsavel',
            name='contratos',
            field=models.ManyToManyField(blank=True, related_name='responsavel', to='administrativo.ContratoEducacional'),
        ),
    ]