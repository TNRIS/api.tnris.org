# Generated by Django 2.0.6 on 2018-11-09 16:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0024_auto_20181105_0902'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountyRelate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('area_type_id', models.ForeignKey(db_column='area_type_id', on_delete=django.db.models.deletion.CASCADE, related_name='AreaType', to='lcd.AreaType')),
                ('collection_id', models.ForeignKey(db_column='collection_id', on_delete=django.db.models.deletion.CASCADE, related_name='Collections', to='lcd.Collection')),
            ],
            options={
                'verbose_name_plural': 'County Relate',
                'db_table': 'collection_county_relate',
            },
        ),
        migrations.AlterUniqueTogether(
            name='countyrelate',
            unique_together={('collection_id', 'area_type_id')},
        ),
    ]