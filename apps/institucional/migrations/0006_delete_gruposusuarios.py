# Generated by Django 3.2.7 on 2021-10-11 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institucional', '0005_remove_gruposusuarios_pedagogico_disciplinas'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GruposUsuarios',
        ),
    ]
