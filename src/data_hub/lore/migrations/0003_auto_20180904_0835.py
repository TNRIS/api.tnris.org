# Generated by Django 2.0.6 on 2018-09-04 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lore', '0002_auto_20180822_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChcView',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, verbose_name='Historical Collection ID')),
                ('collection', models.CharField(max_length=24, verbose_name='Collection')),
                ('from_date', models.DateField(verbose_name='From Date')),
                ('to_date', models.DateField(verbose_name='To Date')),
                ('public', models.BooleanField(verbose_name='Public')),
                ('index_service_url', models.CharField(max_length=256, verbose_name='Index Service URL')),
                ('frames_service_url', models.CharField(max_length=256, verbose_name='Frames Service URL')),
                ('mosaic_service_url', models.CharField(max_length=256, verbose_name='Mosaic Service URL')),
                ('ls4_link', models.CharField(max_length=200, verbose_name='LS4 Link Identifer')),
                ('counties', models.TextField(verbose_name='Counties')),
                ('name', models.CharField(max_length=254, verbose_name='Acquiring Agency Name')),
                ('abbreviation', models.CharField(max_length=20, verbose_name='Acquiring Agency Abbreviation')),
                ('products', models.TextField(verbose_name='Products')),
            ],
            options={
                'verbose_name': 'Compiled Historical Collection',
                'verbose_name_plural': 'Compiled Historical Collections',
                'db_table': 'compiled_historical_collection',
                'managed': False,
            },
        ),
        migrations.RemoveField(
            model_name='photoindex',
            name='service_url',
        ),
        migrations.AddField(
            model_name='collection',
            name='frames_service_url',
            field=models.URLField(blank=True, max_length=256, null=True, verbose_name='Frames Service URL'),
        ),
        migrations.AddField(
            model_name='collection',
            name='index_service_url',
            field=models.URLField(blank=True, max_length=256, null=True, verbose_name='Index Service URL'),
        ),
        migrations.AddField(
            model_name='collection',
            name='ls4_link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='mosaic_service_url',
            field=models.URLField(blank=True, max_length=256, null=True, verbose_name='Mosaic Service URL'),
        ),
    ]