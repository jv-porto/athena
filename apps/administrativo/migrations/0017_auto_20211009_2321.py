# Generated by Django 3.2.7 on 2021-10-10 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0016_alter_escola_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='arquivo',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='digitalizacao',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='escola',
            name='logo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pessoacolaborador',
            name='foto',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pessoaestudante',
            name='foto',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pessoaresponsavel',
            name='foto',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]