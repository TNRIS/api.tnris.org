# Generated by Django 2.0.6 on 2018-08-17 12:46

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0005_resource_resource_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceTypeRelate',
            fields=[
                ('resource_type_relate_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Resource Type Relate ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('collection_id', models.ForeignKey(db_column='collection_id', on_delete=django.db.models.deletion.CASCADE, related_name='resource_type_collections', to='lcd.Collection')),
                ('resource_type_id', models.ForeignKey(db_column='resource_type_id', on_delete=django.db.models.deletion.CASCADE, related_name='resource_type', to='lcd.ResourceType')),
            ],
            options={
                'verbose_name': 'Resource Type Lookup',
                'verbose_name_plural': 'Resource Type Lookups',
                'db_table': 'resource_type_relate',
            },
        ),
        migrations.AlterUniqueTogether(
            name='resourcetyperelate',
            unique_together={('resource_type_id', 'collection_id')},
        ),
    ]