# Generated by Django 3.2.7 on 2021-10-16 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0025_auto_20211015_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoacolaborador',
            name='contratos',
            field=models.ManyToManyField(blank=True, related_name='colaborador', to='administrativo.ContratoTrabalhista'),
        ),
        migrations.AlterField(
            model_name='pessoaestudante',
            name='contratos',
            field=models.ManyToManyField(blank=True, related_name='estudante', to='administrativo.ContratoEducacional'),
        ),
        migrations.AlterField(
            model_name='pessoaresponsavel',
            name='contratos',
            field=models.ManyToManyField(blank=True, related_name='responsavel', to='administrativo.ContratoEducacional'),
        ),
    ]
