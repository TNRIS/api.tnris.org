# Generated by Django 2.0.13 on 2019-08-07 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tnris_org', '0013_auto_20190807_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tnrisinstructor',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='Instructor Bio'),
        ),
        migrations.AlterField(
            model_name='tnrisinstructor',
            name='headshot',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Image URL'),
        ),
    ]