# Generated by Django 2.0.13 on 2019-10-11 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0019_auto_20191011_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='texasimageryservicerequest',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Active?'),
        ),
    ]