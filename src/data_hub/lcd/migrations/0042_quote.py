# Generated by Django 2.0.13 on 2019-11-19 20:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0041_auto_20191016_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('quote_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Quote ID')),
                ('author', models.CharField(max_length=80, verbose_name='Author')),
                ('quote', models.TextField(verbose_name='Quote')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
            ],
            options={
                'verbose_name': 'Quote',
                'verbose_name_plural': 'Quotes',
                'db_table': 'quote_log',
                'ordering': ('author',),
            },
        ),
    ]