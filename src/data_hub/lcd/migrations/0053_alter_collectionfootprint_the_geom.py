# Generated by Django 3.2.5 on 2021-08-10 20:12

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.collections
import django.contrib.gis.geos.polygon
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0052_alter_collectionfootprint_the_geom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionfootprint',
            name='the_geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(default=django.contrib.gis.geos.collections.MultiPolygon(django.contrib.gis.geos.polygon.Polygon(((-107.05078125, 25.60190226111573), (-93.07617187499999, 25.60190226111573), (-93.07617187499999, 36.66841891894786), (-107.05078125, 36.66841891894786), (-107.05078125, 25.60190226111573)))), null=True, srid=4326, verbose_name='The Geometry'),
        ),
    ]