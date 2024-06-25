# Generated by Django 1.10.2 on 2016-12-12 03:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ips4User',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='ips4', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(max_length=254)),
                ('id', models.CharField(max_length=254)),
            ],
        ),
    ]