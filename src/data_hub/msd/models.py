# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
import boto3

from django.db import models


"""
********** Domain Tables **********
"""

class MapSize(models.Model):
    """Domain defining map dimensions"""
    class Meta:
        db_table = 'map_size'
        verbose_name = 'Map Size'
        verbose_name_plural = 'Map Sizes'
        unique_together = ('length', 'width')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField('Label', max_length=35, unique=True, help_text='35 Character Limit')
    length = models.DecimalField('Length', max_digits=5, decimal_places=2, help_text='Inches')
    width = models.DecimalField('Width', max_digits=5, decimal_places=2, help_text='Inches')
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return '%s - %sx%s' % (self.label, str(self.width), str(self.length))


class PixelsPerInch(models.Model):
    """Domain defining PPI intensities"""
    class Meta:
        db_table = 'pixels_per_inch'
        verbose_name = 'Pixels Per Inch'
        verbose_name_plural = 'Pixels Per Inch'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pixels_per_inch = models.PositiveIntegerField('Pixels Per Inch', unique=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return '%sppi' % (str(self.pixels_per_inch))


"""
********** Lookup Tables **********
"""


class MapDataRelate(models.Model):
    """
    Defines data collections from LCD that are associated with a map.
    """

    class Meta:
        db_table = 'map_data_relate'
        verbose_name = 'Map Data Lookup'
        verbose_name_plural = 'Map Data Lookups'
        unique_together = (
            'data_collection_id',
            'map_collection_id'
        )

    map_data_relate_id = models.UUIDField(
        'Map Data Relate ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    map_collection_id = models.ForeignKey(
        'MapCollection',
        db_column='map_collection_id',
        on_delete=models.CASCADE,
        related_name='map_collection'
    )
    data_collection_id = models.ForeignKey(
        'lcd.Collection',
        db_column='collection_id',
        on_delete=models.CASCADE,
        related_name='data_collection'
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        'Last Modified',
        auto_now=True
    )

    def __str__(self):
        return str(self.map_collection_id) + "_" + str(self.data_collection_id)


"""
********** Primary Tables **********
"""

class MapCollection(models.Model):
    """
    Defines distinct map collections/series
    """

    class Meta:
        db_table = 'map_collection'
        verbose_name = 'Map Collection'
        verbose_name_plural = 'Map Collections'
        ordering = ('name',)

    map_collection_id = models.UUIDField(
        'Map Collection ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        'Name',
        max_length=100,
        null=False,
        blank=False
    )
    publish_date = models.DateField(
        'Publish Date',
        null=False,
        blank=False
    )
    description = models.TextField(
        'Description',
        null=True,
        blank=True
    )
    thumbnail_link = models.URLField(
        'Thumbnail Link',
        max_length=255,
        null=True,
        blank=True
    )
    public = models.BooleanField(
        'Public',
        default=False
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        'Last Modified',
        auto_now=True
    )

    def delete_s3_files(self):
        # do that boto dance
        client = boto3.client('s3')
        # set aside list for compiling keys
        key_list = []
        # list Objects
        collection_prefix = str(self.map_collection_id) + '/assets'
        response = client.list_objects_v2(
            Bucket='data.tnris.org',
            Prefix=collection_prefix
        )
        if 'Contents' in response.keys():
            # add image keys to list
            for file in response['Contents']:
                key_list.append({'Key':file['Key']})
            response = client.delete_objects(
                Bucket='data.tnris.org',
                Delete={'Objects': key_list}
            )
            print('%s s3 files: delete success!' % self.name)
        return

    # overwrite default model delete method so that all associated
    # s3 files get deleted as well
    def delete(self, *args, **kwargs):
        self.delete_s3_files()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class MapDownload(models.Model):
    """
    Defines available map download resources (PDF).
    """

    class Meta:
        db_table = 'map_download'
        verbose_name = 'Map Download'
        verbose_name_plural = 'Map Downloads'
        unique_together = (
            'map_collection_id',
            'download_url'
        )

    map_download_id = models.UUIDField(
        'Map Download ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    map_collection_id = models.ForeignKey(
        'MapCollection',
        db_column='map_collection_id',
        on_delete=models.CASCADE,
        related_name='map_collection_download'
    )
    map_size = models.ForeignKey(
        'MapSize',
        on_delete=models.CASCADE,
        related_name='map_collection_download'
    )
    pixels_per_inch = models.ForeignKey(
        'PixelsPerInch',
        on_delete=models.CASCADE,
        related_name='map_collection_download'
    )
    download_url = models.URLField(
        'Download URL',
        max_length=350
    )
    label = models.CharField(
        'Map Label',
        max_length=100,
        null=False,
        blank=False
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        'Last Modified',
        auto_now=True
    )
    # delete s3 image files
    def delete(self, *args, **kwargs):
        client = boto3.client('s3')
        key = str(self).replace('https://s3.amazonaws.com/data.tnris.org/', '')
        response = client.delete_object(
            Bucket='data.tnris.org',
            Key=key
        )
        print(self)
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.download_url)


"""
********** Database Views **********
**** Used as the API endpoints ****
"""

class MsdView(models.Model):
    """
    Master Systems Display view presents MapCollection table with all
    associated relates joined
    """

    class Meta:
        managed = False
        db_table = "master_systems_display"
        verbose_name = 'Master Systems Display'
        verbose_name_plural = 'Master Systems Display'

    collection_id = models.UUIDField(
        'Map Collection ID',
        primary_key=True
    )
    name = models.CharField(
        'Name',
        max_length=100
    )
    publish_date = models.DateField(
        'Publish Date'
    )
    description = models.TextField(
        'Description'
    )
    thumbnail_link = models.CharField(
        'Thumbnail Link',
        max_length=255
    )
    public = models.BooleanField(
        'Public'
    )
    data_collections = models.TextField(
        'Data Collections'
    )
    map_downloads = models.TextField(
        'Map Downloads'
    )

    def __str__(self):
        return self.name
