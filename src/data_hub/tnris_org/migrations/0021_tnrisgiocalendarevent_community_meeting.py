# Generated by Django 2.0.13 on 2019-08-19 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tnris_org', '0020_auto_20190819_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='tnrisgiocalendarevent',
            name='community_meeting',
            field=models.BooleanField(default=False, verbose_name='Community Meeting'),
        ),
    ]