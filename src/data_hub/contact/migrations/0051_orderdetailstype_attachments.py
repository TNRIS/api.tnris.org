# Generated by Django 3.2.14 on 2023-03-27 19:05

import contact.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0050_alter_orderdetailstype_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetailstype',
            name='attachments',
            field=contact.fields.ProtectedImageField(default='', max_length=104, verbose_name='Attached Files.'),
        ),
    ]