# Generated by Django 1.11.6 on 2017-12-23 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0015_user_profiles'),
        ('auth', '0008_alter_user_username_max_length'),
        ('eveonline', '0009_on_delete'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutogroupsConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corp_groups', models.BooleanField(default=False, help_text='Setting this to false will delete all the created groups.')),
                ('corp_group_prefix', models.CharField(blank=True, default='Corp ', max_length=50)),
                ('corp_name_source', models.CharField(choices=[('ticker', 'Ticker'), ('name', 'Full name')], default='name', max_length=20)),
                ('alliance_groups', models.BooleanField(default=False, help_text='Setting this to false will delete all the created groups.')),
                ('alliance_group_prefix', models.CharField(blank=True, default='Alliance ', max_length=50)),
                ('alliance_name_source', models.CharField(choices=[('ticker', 'Ticker'), ('name', 'Full name')], default='name', max_length=20)),
                ('replace_spaces', models.BooleanField(default=False)),
                ('replace_spaces_with', models.CharField(blank=True, default='', help_text='Any spaces in the group name will be replaced with this.', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ManagedAllianceGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alliance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eveonline.EveAllianceInfo')),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eve_autogroups.AutogroupsConfig')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ManagedCorpGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eve_autogroups.AutogroupsConfig')),
                ('corp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eveonline.EveCorporationInfo')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='autogroupsconfig',
            name='alliance_managed_groups',
            field=models.ManyToManyField(help_text="A list of alliance groups created and maintained by this AutogroupConfig. You should not edit this list unless you know what you're doing.", related_name='alliance_managed_config', through='eve_autogroups.ManagedAllianceGroup', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='autogroupsconfig',
            name='corp_managed_groups',
            field=models.ManyToManyField(help_text="A list of corporation groups created and maintained by this AutogroupConfig. You should not edit this list unless you know what you're doing.", related_name='corp_managed_config', through='eve_autogroups.ManagedCorpGroup', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='autogroupsconfig',
            name='states',
            field=models.ManyToManyField(related_name='autogroups', to='authentication.State'),
        ),
    ]