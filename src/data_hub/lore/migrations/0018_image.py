# Generated by Django 2.0.13 on 2020-04-29 14:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('lore', '0017_delete_scale'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Image ID')),
                ('image_url', models.URLField(max_length=255, verbose_name='Image URL')),
                ('caption', models.CharField(blank=True, max_length=255, null=True, verbose_name='Image Caption')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('collection_id', models.ForeignKey(db_column='collection_id', on_delete=django.db.models.deletion.CASCADE, related_name='image_collections', to='lore.Collection')),
            ],
            options={
                'verbose_name': 'Historical Image',
                'verbose_name_plural': 'Historical Images',
                'db_table': 'historical_image',
            },
        ),
    ]