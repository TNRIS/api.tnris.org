# Generated by Django 2.0.6 on 2018-07-27 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='acquisition_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Acquisiiton Date'),
        ),
    ]