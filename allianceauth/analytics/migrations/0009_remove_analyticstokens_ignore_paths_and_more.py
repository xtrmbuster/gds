# Generated by Django 4.0.10 on 2023-05-08 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0008_add_AA_GA-4_Team_Token '),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analyticstokens',
            name='ignore_paths',
        ),
        migrations.RemoveField(
            model_name='analyticstokens',
            name='send_celery_tasks',
        ),
        migrations.RemoveField(
            model_name='analyticstokens',
            name='send_page_views',
        ),
        migrations.DeleteModel(
            name='AnalyticsPath',
        ),
    ]
