# Generated by Django 3.2.7 on 2022-01-14 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0037_auto_20220113_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoacolaborador',
            name='nacionalidade',
            field=models.CharField(default='Brasileiro(a)', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pessoacolaborador',
            name='profissao',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pessoaestudante',
            name='nacionalidade',
            field=models.CharField(default='Brasileiro(a)', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pessoaestudante',
            name='profissao',
            field=models.CharField(default='Estudante', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pessoaresponsavel',
            name='nacionalidade',
            field=models.CharField(default='Brasileiro(a)', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pessoaresponsavel',
            name='profissao',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
    ]
