# Generated by Django 1.10.1 on 2016-09-06 23:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fleetactivitytracking', '0002_auto_20160905_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fatlink',
            name='fatdatetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
