# Generated by Django 3.2.5 on 2022-02-25 13:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0040_auto_20201124_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('campaign_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='subscriber identification number')),
                ('campaign_name', models.CharField(max_length=40, unique=True, verbose_name='human friendly name for campaign')),
                ('campaign_description', models.CharField(max_length=140, verbose_name='description of campaign, including limitations for use of emails, etc')),
            ],
            options={
                'verbose_name': 'Campaign',
                'verbose_name_plural': ('Campaigns',),
                'db_table': 'campaign',
                'ordering': ['campaign_name'],
            },
        ),
        migrations.CreateModel(
            name='CampaignSubscriber',
            fields=[
                ('subscriber_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='subscriber identification number')),
                ('email', models.EmailField(editable=False, max_length=254, unique=True, verbose_name='email')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contact.campaign')),
            ],
            options={
                'verbose_name': 'Campaign Subscriber',
                'verbose_name_plural': ('Campaign Subscribers',),
                'db_table': 'campaign_subscriber',
                'ordering': ['campaign__campaign_name'],
            },
        ),
    ]