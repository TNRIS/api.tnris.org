# Generated by Django 3.0.8 on 2020-12-15 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tnris_org', '0032_auto_20201214_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tnrisdocument',
            name='document_name',
            field=models.CharField(help_text='Plain text label, title, or name for the file. Must be unique.', max_length=200, unique=True, verbose_name='Document Name'),
        ),
        migrations.AlterField(
            model_name='tnrisdocument',
            name='document_url',
            field=models.URLField(max_length=255, unique=True, verbose_name='Document URL'),
        ),
    ]