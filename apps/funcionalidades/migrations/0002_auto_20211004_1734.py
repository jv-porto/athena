# Generated by Django 3.2.7 on 2021-10-04 20:34

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionalidades', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='anexos',
            field=models.FileField(blank=True, upload_to='emails/anexos/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='email',
            name='ccs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254), blank=True, default=[], size=None),
            preserve_default=False,
        ),
    ]
