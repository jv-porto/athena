# Generated by Django 3.2.7 on 2021-10-24 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0031_modulosescola_institucional_integracoes'),
        ('institucional', '0012_integracoes'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntegracaoContaAzul',
            fields=[
                ('descricao', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('access_token', models.CharField(max_length=100)),
                ('refresh_token', models.CharField(max_length=100)),
                ('expires_in', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('escola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrativo.escola')),
            ],
        ),
    ]
