# Generated by Django 2.0.8 on 2019-02-15 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0036_delete_agencytype'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcetype',
            name='source_data_website',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Source Data Website'),
        ),
    ]