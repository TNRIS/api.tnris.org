# Generated by Django 2.0.13 on 2019-07-10 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tnris_org', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tnrisdocurl',
            name='doc_name',
            field=models.CharField(editable=False, max_length=200, verbose_name='Document Name'),
        ),
        migrations.AlterField(
            model_name='tnrisimageurl',
            name='image_name',
            field=models.CharField(editable=False, max_length=200, verbose_name='Image Name'),
        ),
    ]
