# Generated by Django 1.10.5 on 2017-03-22 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleetactivitytracking', '0003_auto_20160906_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fatlink',
            name='fleet',
            field=models.CharField(default='', max_length=254),
        ),
    ]
