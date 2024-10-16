# Generated by Django 3.2.14 on 2022-08-19 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lcd', '0055_auto_20210811_0910'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceTypeCategory',
            fields=[
                ('category_name', models.TextField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
            ],
            options={
                'verbose_name': 'Resource Type Category',
                'verbose_name_plural': 'Resource Type Categories',
                'db_table': 'resource_type_category',
            },
        ),
        migrations.AddField(
            model_name='resourcetype',
            name='resource_type_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lcd.resourcetypecategory'),
        ),
    ]
