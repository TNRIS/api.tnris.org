# Generated by Django 3.2.5 on 2021-08-10 20:35

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0053_alter_collectionfootprint_the_geom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionfootprint',
            name='the_geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(default=None, null=True, srid=4326, verbose_name='The Geometry'),
        ),
    ]