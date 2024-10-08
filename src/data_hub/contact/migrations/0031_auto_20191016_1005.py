# Generated by Django 2.0.13 on 2019-10-16 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0030_auto_20191014_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='serializer_classname',
            field=models.CharField(help_text="Serializer classname from serializers.py file. Must be exact. Typically is: '<-ModelClassname->Serializer'", max_length=70, unique=True, verbose_name='Serializer Classname'),
        ),
    ]
