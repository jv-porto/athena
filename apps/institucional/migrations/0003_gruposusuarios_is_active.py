# Generated by Django 3.2.7 on 2021-10-05 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institucional', '0002_gruposusuarios_escola'),
    ]

    operations = [
        migrations.AddField(
            model_name='gruposusuarios',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
