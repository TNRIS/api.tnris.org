# Generated by Django 2.0.13 on 2019-10-16 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0040_xlargesupplemental'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='lidar_buildings_url',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Lidar Buildings URL'),
        ),
        migrations.AlterUniqueTogether(
            name='collection',
            unique_together={('name', 'acquisition_date', 'authoritative', 'public', 'known_issues', 'md_filename', 'wms_link', 'popup_link', 'carto_map_id', 'thumbnail_image', 'tile_index_url', 'supplemental_report_url', 'lidar_breaklines_url', 'lidar_buildings_url', 'coverage_extent', 'tags', 'license_type_id', 'source_type_id', 'template_type_id')},
        ),
    ]