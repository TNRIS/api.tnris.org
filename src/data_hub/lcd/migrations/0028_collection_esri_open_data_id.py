# Generated by Django 2.0.8 on 2018-12-07 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0027_categorytype_filter_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='esri_open_data_id',
            field=models.TextField(blank=True, db_column='esri_open_data_id', null=True, verbose_name='ESRI Open Data ID'),
        ),
    ]
