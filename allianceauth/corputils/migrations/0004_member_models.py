# Generated by Django 1.10.5 on 2017-03-26 20:13

from django.db import migrations, models
import django.db.models.deletion
import json


def convert_json_to_members(apps, schema_editor):
    CorpStats = apps.get_model('corputils', 'CorpStats')
    CorpMember = apps.get_model('corputils', 'CorpMember')
    for cs in CorpStats.objects.all():
        members = json.loads(cs._members)
        CorpMember.objects.bulk_create(
            [CorpMember(corpstats=cs, character_id=member_id, character_name=member_name) for member_id, member_name in members.items()]
        )


def convert_members_to_json(apps, schema_editor):
    CorpStats = apps.get_model('corputils', 'CorpStats')
    for cs in CorpStats.objects.all():
        cs._members = json.dumps({m.character_id: m.character_name for m in cs.members.all()})
        cs.save()


class Migration(migrations.Migration):
    dependencies = [
        ('corputils', '0003_granular_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorpMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_id', models.PositiveIntegerField()),
                ('character_name', models.CharField(max_length=37)),
            ],
            options={
                'ordering': ['character_name'],
            },
        ),
        migrations.AddField(
            model_name='corpmember',
            name='corpstats',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members',
                                    to='corputils.CorpStats'),
        ),
        migrations.AlterUniqueTogether(
            name='corpmember',
            unique_together={('corpstats', 'character_id')},
        ),
        migrations.RunPython(convert_json_to_members, convert_members_to_json),
        migrations.RemoveField(
            model_name='corpstats',
            name='_members',
        ),
    ]