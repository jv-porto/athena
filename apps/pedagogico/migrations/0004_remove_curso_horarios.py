# Generated by Django 3.2.7 on 2021-10-07 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedagogico', '0003_auto_20211006_2058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curso',
            name='horarios',
        ),
    ]
