# Generated by Django 2.0.13 on 2020-01-31 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tnris_org', '0023_tnrisgiocalendarevent_community_meeting_agenda_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='tnrisdocument',
            name='sgm_note',
            field=models.BooleanField(default=False, verbose_name='Solutions Group Note'),
        ),
    ]