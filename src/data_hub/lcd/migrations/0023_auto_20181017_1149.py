# Generated by Django 2.0.6 on 2018-10-17 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0022_auto_20181017_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='natural_image',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='overview_image',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='urban_image',
        ),
    ]
