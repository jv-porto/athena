# Generated by Django 3.2.7 on 2021-10-01 03:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0009_auto_20211001_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='data_assinatura',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
