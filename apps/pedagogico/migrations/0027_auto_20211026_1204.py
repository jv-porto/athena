# Generated by Django 3.2.7 on 2021-10-26 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedagogico', '0026_auto_20211026_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curso',
            name='parcelamento_curso',
        ),
        migrations.RemoveField(
            model_name='curso',
            name='parcelamento_material',
        ),
        migrations.RemoveField(
            model_name='curso',
            name='valor_curso',
        ),
        migrations.RemoveField(
            model_name='curso',
            name='valor_material',
        ),
        migrations.AlterField(
            model_name='turma',
            name='parcelamento_curso',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='turma',
            name='parcelamento_material',
            field=models.CharField(blank=True, max_length=2),
        ),
    ]
