# Generated by Django 3.2.7 on 2021-10-24 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institucional', '0015_remove_integracaocontaazul_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='integracaocontaazul',
            name='is_active',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
