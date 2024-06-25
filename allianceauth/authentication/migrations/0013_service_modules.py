# Generated by Django 1.10.2 on 2016-12-11 23:14

from django.db import migrations

import logging

logger = logging.getLogger(__name__)


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_remove_add_delete_authservicesinfo_permissions'),
    ]

    operations = [
        # Remove fields
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='discord_uid',
        ),
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='discourse_enabled',
        ),
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='forum_username',
        ),
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='ipboard_username',
        ),
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='ips4_id',
        ),
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='ips4_username',
        ),
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='jabber_username',
        ),
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='market_username',
        ),
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='mumble_username',
        ),
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='smf_username',
        ),
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='teamspeak3_perm_key',
        ),
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='teamspeak3_uid',
        ),
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='xenforo_username',
        ),
    ]