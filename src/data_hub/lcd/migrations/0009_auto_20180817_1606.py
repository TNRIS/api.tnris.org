# Generated by Django 2.0.6 on 2018-08-17 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0008_auto_20180817_1542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resource',
            old_name='resource_type',
            new_name='resource_type_id',
        ),
    ]