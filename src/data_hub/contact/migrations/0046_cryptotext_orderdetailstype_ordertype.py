# Generated by Django 3.2.14 on 2023-02-03 21:23

import contact.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0045_alter_campaignsubscriber_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cryptoText', contact.fields.CryptoTextField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetailsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', contact.fields.CryptoTextField(max_length=500000, verbose_name='Details')),
            ],
            options={
                'verbose_name': 'Order Details Type',
                'verbose_name_plural': 'Order DetailsTypes',
                'db_table': 'order_details_type',
            },
        ),
        migrations.CreateModel(
            name='OrderType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Order Id')),
                ('order_token', models.UUIDField(default=None, editable=False, null=True, verbose_name='Order Token')),
                ('order_url', models.CharField(default=None, editable=False, max_length=255, null=True, verbose_name='Order url')),
                ('order_approved', models.BooleanField(default=False, verbose_name='Order approved?')),
                ('received_receipt', models.BooleanField(blank=True, default=False, editable=False, null=True, verbose_name='Receipt Received')),
                ('approved_charge', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Approved Charge')),
                ('archived', models.BooleanField(default=False, verbose_name='Order Archived?')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('order_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contact.orderdetailstype')),
            ],
            options={
                'verbose_name': 'Order Type',
                'verbose_name_plural': 'Order Types',
                'db_table': 'order_type',
            },
        ),
    ]