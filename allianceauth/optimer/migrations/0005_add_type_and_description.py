# Generated by Django 3.2.8 on 2021-10-26 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("optimer", "0004_on_delete"),
    ]

    operations = [
        migrations.CreateModel(
            name="OpTimerType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(default="", max_length=254)),
            ],
            options={
                "ordering": ["type"],
                "default_permissions": (),
            },
        ),
        migrations.AlterModelOptions(
            name="optimer",
            options={"default_permissions": (), "ordering": ["start"]},
        ),
        migrations.AddField(
            model_name="optimer",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="optimer",
            name="type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="optimer.optimertype",
            ),
        ),
    ]