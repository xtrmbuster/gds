# Generated by Django 1.11.5 on 2017-09-28 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eveonline', '0008_remove_apikeys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evecorporationinfo',
            name='alliance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='eveonline.EveAllianceInfo'),
        ),
    ]