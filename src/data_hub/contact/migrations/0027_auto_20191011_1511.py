# Generated by Django 2.0.13 on 2019-10-11 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0026_emailtemplate_serializer_classname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='serializer_classname',
            field=models.CharField(help_text='Serializer classname from serializers.py file. Must be exact.', max_length=70, unique=True, verbose_name='Serializer Classname'),
        ),
    ]