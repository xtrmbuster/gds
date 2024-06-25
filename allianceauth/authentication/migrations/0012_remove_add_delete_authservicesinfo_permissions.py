# Generated by Django 1.10.5 on 2017-01-12 00:59

from django.db import migrations, models

def remove_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Permission = apps.get_model('auth', 'Permission')
    AuthServicesInfo = apps.get_model('authentication', 'AuthServicesInfo')

    # delete the add and remove permissions for AuthServicesInfo
    ct = ContentType.objects.get_for_model(AuthServicesInfo)
    Permission.objects.filter(content_type=ct).filter(codename__in=['add_authservicesinfo', 'delete_authservicesinfo']).delete()


def add_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Permission = apps.get_model('auth', 'Permission')
    AuthServicesInfo = apps.get_model('authentication', 'AuthServicesInfo')

    # recreate the add and remove permissions for AuthServicesInfo
    ct = ContentType.objects.get_for_model(AuthServicesInfo)
    Permission.objects.create(content_type=ct, codename='add_authservicesinfo', name='Can add auth services info')
    Permission.objects.create(content_type=ct, codename='delete_authservicesinfo', name='Can delete auth services info')

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_authservicesinfo_user_onetoonefield'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authservicesinfo',
            options={'default_permissions': ('change',)},
        ),
        migrations.RunPython(remove_permissions, add_permissions),
    ]