# Generated by Django 3.1.2 on 2020-10-25 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("groupmanagement", "0014_auto_20200918_1412"),
    ]

    operations = [
        migrations.AlterField(
            model_name="authgroup",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="Short description <i>(max. 512 characters)</i> of the group shown to users.",
                max_length=512,
            ),
        ),
    ]
