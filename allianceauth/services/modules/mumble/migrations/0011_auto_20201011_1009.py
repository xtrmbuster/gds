# Generated by Django 3.1.2 on 2020-10-11 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mumble', '0010_mumbleuser_certhash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mumbleuser',
            name='pwhash',
            field=models.CharField(max_length=90),
        ),
    ]
