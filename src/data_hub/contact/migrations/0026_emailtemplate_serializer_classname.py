# Generated by Django 2.0.13 on 2019-10-11 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0025_auto_20191011_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtemplate',
            name='serializer_classname',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Serializer Classname'),
        ),
    ]