# Generated by Django 3.2.7 on 2021-10-11 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0020_alter_modulosescola_escola'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulosescola',
            name='institucional_usuarios_permissoes',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
