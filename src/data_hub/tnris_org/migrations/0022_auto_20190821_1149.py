# Generated by Django 2.0.13 on 2019-08-21 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tnris_org', '0021_tnrisgiocalendarevent_community_meeting'),
    ]

    operations = [
        migrations.AddField(
            model_name='tnrisgiocalendarevent',
            name='solutions_group_meeting',
            field=models.BooleanField(default=False, verbose_name='Solutions Group Meeting'),
        ),
        migrations.AlterField(
            model_name='tnrisgiocalendarevent',
            name='public',
            field=models.BooleanField(default=False, help_text='Display on website!', verbose_name='Public'),
        ),
    ]