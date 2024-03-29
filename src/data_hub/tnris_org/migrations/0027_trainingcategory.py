# Generated by Django 2.0.13 on 2020-05-18 18:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tnris_org', '0026_auto_20200504_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingCategory',
            fields=[
                ('training_category_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Category ID')),
                ('training_category', models.CharField(max_length=100, verbose_name='Category')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
            ],
            options={
                'verbose_name': 'Tnris Training Category',
                'verbose_name_plural': 'Tnris Training Categories',
                'db_table': 'tnris_training_category',
                'ordering': ('training_category',),
            },
        ),
    ]
