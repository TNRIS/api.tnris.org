# Generated by Django 2.0.13 on 2019-07-16 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tnris_org', '0006_auto_20190716_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='tnrisforumtraining',
            name='public',
            field=models.BooleanField(default=False, verbose_name='Public'),
        ),
        migrations.AddField(
            model_name='tnristraining',
            name='public',
            field=models.BooleanField(default=False, verbose_name='Public'),
        ),
        migrations.AlterField(
            model_name='tnrisforumtraining',
            name='max_students',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='Max Student Amount'),
        ),
        migrations.AlterField(
            model_name='tnrisforumtraining',
            name='teaser',
            field=models.TextField(blank=True, verbose_name='Training Teaser'),
        ),
    ]
