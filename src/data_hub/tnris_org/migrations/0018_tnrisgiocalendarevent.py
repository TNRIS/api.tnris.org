# Generated by Django 2.0.13 on 2019-08-19 16:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tnris_org', '0017_completeforumtrainingview'),
    ]

    operations = [
        migrations.CreateModel(
            name='TnrisGioCalendarEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Event ID')),
                ('start_date', models.DateField(verbose_name='Event Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Event End Date')),
                ('start_time', models.TimeField(verbose_name='Event Start Time')),
                ('end_time', models.TimeField(verbose_name='Event End Time')),
                ('title', models.CharField(max_length=255, verbose_name='Event Title')),
                ('short_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Short Description')),
                ('location', models.CharField(blank=True, max_length=150, null=True, verbose_name='Event Location')),
                ('street_address', models.CharField(blank=True, max_length=150, null=True, verbose_name='Street Address')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='City')),
                ('state', models.CharField(blank=True, max_length=2, null=True, verbose_name='State Abbreviation')),
                ('zipcode', models.CharField(blank=True, max_length=10, null=True, verbose_name='State Abbreviation')),
                ('event_url', models.URLField(blank=True, max_length=255, null=True, verbose_name='Event URL')),
                ('public', models.BooleanField(default=False, verbose_name='Public')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
            ],
            options={
                'verbose_name': 'Tnris GIO Calendar Event',
                'verbose_name_plural': 'Tnris GIO Calendar Events',
                'db_table': 'tnris_gio_calendar_event',
            },
        ),
    ]
