# Generated by Django 3.0.8 on 2020-08-25 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lore', '0021_auto_20200825_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='thumbnail_image',
            field=models.TextField(blank=True, default='https://s3.amazonaws.com/data.tnris.org/historical_images/historical_thumbnail.jpg', max_length=200, null=True, verbose_name='Thumb Image'),
        ),
    ]