# Generated by Django 2.0.6 on 2018-11-13 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lore', '0006_scannedphotoindexlink_sheet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='physical_location',
            field=models.TextField(blank=True, null=True, verbose_name='Physical Location'),
        ),
    ]
