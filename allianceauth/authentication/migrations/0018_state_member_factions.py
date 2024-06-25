# Generated by Django 3.1.13 on 2021-10-12 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eveonline', '0015_factions'),
        ('authentication', '0017_remove_fleetup_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='member_factions',
            field=models.ManyToManyField(blank=True, help_text='Factions to whose members this state is available.', to='eveonline.EveFactionInfo'),
        ),
    ]
