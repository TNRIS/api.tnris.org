# Generated by Django 2.0.6 on 2018-08-15 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0002_auto_20180801_1010'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcdcView',
            fields=[
                ('resource', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Resource')),
                ('name', models.TextField(verbose_name='Name')),
                ('area_type', models.TextField(verbose_name='Area Type')),
                ('area_type_name', models.TextField(verbose_name='Area Type Name')),
                ('area_type_id', models.UUIDField(verbose_name='Area Type Id')),
            ],
            options={
                'verbose_name': 'Area Collection Data Connection',
                'verbose_name_plural': 'Area Collection Data Connections',
                'db_table': 'area_collection_data_connection',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CcrView',
            fields=[
                ('collection_id', models.UUIDField(primary_key=True, serialize=False, verbose_name='Collection ID')),
                ('name', models.TextField(verbose_name='Name')),
                ('acquisition_date', models.TextField(verbose_name='Acquisition Date')),
                ('short_description', models.TextField(verbose_name='Short Description')),
                ('description', models.TextField(verbose_name='Description')),
                ('source', models.TextField(verbose_name='Source')),
                ('authoritative', models.BooleanField(verbose_name='Authoritative')),
                ('public', models.BooleanField(verbose_name='Public')),
                ('known_issues', models.TextField(verbose_name='Known Issues')),
                ('wms_link', models.URLField(verbose_name='WMS Link')),
                ('popup_link', models.URLField(verbose_name='Popup Link')),
                ('carto_map_id', models.TextField(verbose_name='Carto Map ID')),
                ('overview_image', models.TextField(verbose_name='Overview Image')),
                ('thumbnail_image', models.TextField(verbose_name='Thumb Image')),
                ('natural_image', models.TextField(verbose_name='Natural Image')),
                ('urban_image', models.TextField(verbose_name='Urban Image')),
                ('tile_index_url', models.URLField(verbose_name='Tile Index URL')),
                ('supplemental_report_url', models.URLField(verbose_name='Supplemental Report URL')),
                ('lidar_breaklines_url', models.URLField(verbose_name='Lidar Breaklines URL')),
                ('coverage_extent', models.TextField(verbose_name='Coverage Extent')),
                ('tags', models.TextField(verbose_name='Tags')),
                ('band', models.TextField(verbose_name='Band')),
                ('category', models.TextField(verbose_name='Category')),
                ('data_type', models.TextField(verbose_name='Data Type')),
                ('spatial_reference', models.TextField(verbose_name='Spatial Reference')),
                ('file_type', models.TextField(verbose_name='File Type')),
                ('resolution', models.TextField(verbose_name='Resolution')),
                ('recommended_use', models.TextField(verbose_name='Recommended Use')),
                ('agency_name', models.TextField(verbose_name='Agency Name')),
                ('agency_abbreviation', models.TextField(verbose_name='Agency Abbreviation')),
                ('agency_website', models.CharField(max_length=255, verbose_name='Agency Website')),
                ('agency_contact', models.TextField(verbose_name='Agency Contact')),
                ('license_name', models.TextField(verbose_name='License Name')),
                ('license_abbreviation', models.TextField(verbose_name='License Abbreviation')),
                ('license_url', models.CharField(max_length=255, verbose_name='License URL')),
                ('template', models.TextField(verbose_name='Template')),
            ],
            options={
                'verbose_name': 'Collection Catalog Record',
                'verbose_name_plural': 'Collection Catalog Records',
                'db_table': 'collection_catalog_record',
                'managed': False,
            },
        ),
    ]