# Generated by Django 2.0.6 on 2018-08-16 16:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=254, unique=True, verbose_name='Name')),
                ('abbreviation', models.CharField(blank=True, max_length=20, null=True, verbose_name='Abbreviation')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
            ],
            options={
                'verbose_name_plural': 'Acquiring Agencies',
                'db_table': 'agency',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('collection', models.CharField(max_length=24, verbose_name='Collection')),
                ('from_date', models.DateField(blank=True, null=True, verbose_name='From Date')),
                ('to_date', models.DateField(blank=True, null=True, verbose_name='To Date')),
                ('public', models.BooleanField(default=True, verbose_name='Public')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agency', to='lore.Agency')),
            ],
            options={
                'verbose_name_plural': 'Historical Collections',
                'db_table': 'historical_collection',
            },
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fips', models.PositiveIntegerField(unique=True, verbose_name='FIPS')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
            ],
            options={
                'verbose_name_plural': 'counties',
                'db_table': 'county',
            },
        ),
        migrations.CreateModel(
            name='CountyRelate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Collections', to='lore.Collection')),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Counties', to='lore.County')),
            ],
            options={
                'verbose_name_plural': 'County Relate',
                'db_table': 'county_relate',
            },
        ),
        migrations.CreateModel(
            name='FrameSize',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('frame_size', models.PositiveIntegerField(unique=True, verbose_name='Frame Size')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
            ],
            options={
                'verbose_name_plural': 'Frame Sizes',
                'db_table': 'frame_size',
            },
        ),
        migrations.CreateModel(
            name='LineIndex',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lore.Collection')),
            ],
            options={
                'verbose_name': 'Line Index',
                'verbose_name_plural': 'Line Indexes',
                'db_table': 'line_index',
            },
        ),
        migrations.CreateModel(
            name='MicroficheIndex',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lore.Collection')),
            ],
            options={
                'verbose_name': 'Microfiche Index',
                'verbose_name_plural': 'Microfiche Indexes',
                'db_table': 'microfiche_index',
            },
        ),
        migrations.CreateModel(
            name='PhotoIndex',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('number_of_frames', models.PositiveIntegerField(default=1, verbose_name='Number of Frames')),
                ('scanned', models.PositiveIntegerField(default=0, verbose_name='Scanned')),
                ('scanned_location', models.CharField(blank=True, max_length=254, null=True, verbose_name='Scanned Location')),
                ('physical_location', models.CharField(blank=True, max_length=50, null=True, verbose_name='Physical Location')),
                ('service_url', models.URLField(blank=True, max_length=256, null=True, verbose_name='Service URL')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lore.Collection')),
            ],
            options={
                'verbose_name': 'Photo Index',
                'verbose_name_plural': 'Photo Indexes',
                'db_table': 'photo_index',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('coverage', models.CharField(choices=[('Full', 'Full'), ('Partial', 'Partial')], default='Partial', max_length=7, verbose_name='Coverage')),
                ('number_of_frames', models.PositiveIntegerField(default=0, verbose_name='Number of Frames')),
                ('scanned', models.PositiveIntegerField(default=0, verbose_name='Scanned')),
                ('medium', models.CharField(choices=[('Film', 'Film'), ('Print', 'Print')], max_length=5, verbose_name='Medium')),
                ('print_type', models.CharField(choices=[('B&W', 'B&W'), ('CIR', 'CIR'), ('NC', 'NC')], max_length=3, verbose_name='Print Type')),
                ('physical_location', models.CharField(blank=True, max_length=50, null=True, verbose_name='Physical Location')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Products', to='lore.Collection')),
                ('frame_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lore.FrameSize')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': 'Products',
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Scale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('scale', models.PositiveIntegerField(unique=True, verbose_name='Scale')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
            ],
            options={
                'verbose_name_plural': 'Scales',
                'db_table': 'scale',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='scale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lore.Scale'),
        ),
        migrations.AddField(
            model_name='photoindex',
            name='scale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lore.Scale'),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('collection', 'scale', 'frame_size', 'number_of_frames', 'scanned', 'medium', 'physical_location')},
        ),
        migrations.AlterUniqueTogether(
            name='photoindex',
            unique_together={('collection', 'scale', 'number_of_frames', 'scanned', 'physical_location')},
        ),
        migrations.AlterUniqueTogether(
            name='microficheindex',
            unique_together={('id', 'collection')},
        ),
        migrations.AlterUniqueTogether(
            name='lineindex',
            unique_together={('id', 'collection')},
        ),
        migrations.AlterUniqueTogether(
            name='countyrelate',
            unique_together={('collection', 'county')},
        ),
    ]