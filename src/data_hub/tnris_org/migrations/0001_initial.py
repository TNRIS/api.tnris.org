# Generated by Django 2.0.13 on 2019-07-10 14:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TnrisDocUrl',
            fields=[
                ('doc_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Document ID')),
                ('doc_name', models.CharField(max_length=200, verbose_name='Document Name')),
                ('doc_url', models.URLField(max_length=255, verbose_name='Document URL')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
            ],
            options={
                'verbose_name': 'Tnris Document Url',
                'verbose_name_plural': 'Tnris Document Urls',
                'db_table': 'tnris_doc_url',
            },
        ),
        migrations.CreateModel(
            name='TnrisImageUrl',
            fields=[
                ('image_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Image ID')),
                ('image_name', models.CharField(max_length=200, verbose_name='Image Name')),
                ('image_url', models.URLField(max_length=255, verbose_name='Image URL')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
            ],
            options={
                'verbose_name': 'Tnris Image Url',
                'verbose_name_plural': 'Tnris Image Urls',
                'db_table': 'tnris_image_url',
            },
        ),
    ]