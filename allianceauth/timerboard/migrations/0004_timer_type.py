# Generated by Django 3.2.8 on 2021-10-20 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("timerboard", "0003_on_delete"),
    ]

    operations = [
        migrations.AddField(
            model_name="timer",
            name="timer_type",
            field=models.CharField(
                choices=[
                    ("UNSPECIFIED", "Not Specified"),
                    ("SHIELD", "Shield"),
                    ("ARMOR", "Armor"),
                    ("HULL", "Hull"),
                    ("FINAL", "Final"),
                    ("ANCHORING", "Anchoring"),
                    ("UNANCHORING", "Unanchoring"),
                ],
                default="UNSPECIFIED",
                max_length=254,
            ),
        ),
    ]
