# Generated by Django 4.0.6 on 2022-08-30 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0006_more_ignore_paths'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyticstokens',
            name='secret',
            field=models.CharField(blank=True, max_length=254),
        ),
    ]
