# Generated by Django 2.0.8 on 2018-12-07 14:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0028_collection_esri_open_data_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutsideEntityServices',
            fields=[
                ('service_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Service ID')),
                ('service_name', models.TextField(db_column='service_name', verbose_name='Service Name')),
                ('service_url', models.URLField(db_column='service_url', verbose_name='Service URL')),
                ('collection_id', models.ForeignKey(db_column='collection_id', on_delete=django.db.models.deletion.CASCADE, related_name='outside_entity_service_collections', to='lcd.Collection')),
            ],
            options={
                'verbose_name': 'Outside Entity Service',
                'verbose_name_plural': 'Outside Entity Services',
                'db_table': 'outside_entity_services',
            },
        ),
    ]
