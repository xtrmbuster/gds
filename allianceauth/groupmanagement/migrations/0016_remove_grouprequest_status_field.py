# Generated by Django 3.2.8 on 2021-10-19 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("groupmanagement", "0015_make_descriptions_great_again"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="grouprequest",
            name="status",
        ),
    ]
