# Generated by Django 3.2.7 on 2021-10-04 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionalidades', '0003_auto_20211004_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='variaveis',
            field=models.JSONField(blank=True, default={}),
        ),
    ]
