# Generated by Django 2.0.6 on 2018-10-08 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0018_auto_20181005_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='collection_id',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]