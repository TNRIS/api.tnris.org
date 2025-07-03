# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
import boto3

from django.db import models


class Agency(models.Model):
    """Domain defining agencies that acquire collections"""
    class Meta:
        db_table = 'agency'
        verbose_name_plural = 'Acquiring Agencies'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Name', max_length=254, unique=True)
    abbreviation = models.CharField('Abbreviation', max_length=20, null=True,
                                    blank=True)
    sample_image_url = models.URLField('Sample Image URL', max_length=256, null=True, blank=True)
    media_type = models.TextField(null=True, blank=True)
    general_scale = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return str(self.name)


class FrameSize(models.Model):
    """Domain defining allowable frame size values"""

    class Meta:
        db_table = 'frame_size'
        verbose_name_plural = 'Frame Sizes'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    frame_size = models.PositiveIntegerField('Frame Size', unique=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return str(self.frame_size)


class PhotoIndex(models.Model):
    """Defines historical imagery collection photo indexes"""

    class Meta:
        db_table = 'photo_index'
        verbose_name = 'Photo Index'
        verbose_name_plural = 'Photo Indexes'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE)
    number_of_frames = models.PositiveIntegerField('Number of Frames', default=1)
    scanned = models.PositiveIntegerField('Scanned', default=0)
    scanned_location = models.CharField('Scanned Location', max_length=254, null=True, blank=True)
    physical_location = models.CharField('Physical Location', max_length=50, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return ''


class ScannedPhotoIndexLink(models.Model):
    """Manages LS4 uploaded photo index scan links"""

    class Meta:
        db_table = 'photo_index_scanned_ls4_link'
        verbose_name = 'Photo Index Scanned LS4 Link'
        verbose_name_plural = 'Photo Index Scanned LS4 Links'
        unique_together = ('collection', 'link')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE)
    year = models.PositiveIntegerField('Designated Year', null=False)
    size = models.CharField('Labeled Size', max_length=20, null=False)
    sheet = models.CharField('Sheet Number', max_length=20, null=False)
    link = models.URLField('Download Link', null=False)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return str(self.link)


class LineIndex(models.Model):
    """Defines historical imagery collection photo indexes"""

    class Meta:
        db_table = 'line_index'
        verbose_name = 'Line Index'
        verbose_name_plural = 'Line Indexes'
        unique_together = ("id", "collection")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return ''


class MicroficheIndex(models.Model):
    """Defines historical imagery collection photo indexes"""

    class Meta:
        db_table = 'microfiche_index'
        verbose_name = 'Microfiche Index'
        verbose_name_plural = 'Microfiche Indexes'
        unique_together = ("id", "collection")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return ''


class County(models.Model):
    """Texas Counties domain table"""

    class Meta:
        db_table = 'county'
        verbose_name_plural = 'counties'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fips = models.PositiveIntegerField('FIPS', unique=True)
    name = models.CharField('Name', max_length=20)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.name


class CountyRelate(models.Model):
    """Defines which county a collection of historical
    imagery has coverage for
    """

    class Meta:
        db_table = 'county_relate'
        verbose_name_plural = 'County Relate'
        unique_together = ("collection", "county")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE, related_name='Collections')
    county = models.ForeignKey('County', on_delete=models.CASCADE, related_name='Counties')
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.county.name


class Product(models.Model):
    """Defines the different products that make up a distinct collection of
    historical imagery
    """

    class Meta:
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE,
                                   related_name='Products')
    frame_size = models.ForeignKey('FrameSize', on_delete=models.CASCADE)
    COVERAGE_TYPE_CHOICE = (
        ('Full', 'Full'),
        ('Partial', 'Partial')
    )
    coverage = models.CharField('Coverage', max_length=7,
                                choices=COVERAGE_TYPE_CHOICE, default='Partial')
    number_of_frames = models.PositiveIntegerField('Number of Frames',
                                                   default=0)

    MEDIUM_TYPE_CHOICE = (
        ('Film', 'Film'),
        ('Print', 'Print')
    )
    medium = models.CharField('Medium', max_length=5,
                              choices=MEDIUM_TYPE_CHOICE)
    PRINT_TYPE_CHOICE = (
        ('B&W', 'B&W'),
        ('CIR', 'CIR'),
        ('NC', 'NC')
    )
    print_type = models.CharField('Print Type', max_length=3,
                                  choices=PRINT_TYPE_CHOICE)
    clean_status = models.BooleanField('Clean Status', default=False)
    physical_location = models.TextField('Physical Location', null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.print_type + ' Product'


class Collection(models.Model):
    """defines distinct historical imagery collections"""

    class Meta:
        db_table = 'historical_collection'
        verbose_name = 'Historical Collection'
        verbose_name_plural = 'Historical Collections'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection = models.CharField('Collection', max_length=24)
    from_date = models.DateField('From Date', null=True, blank=True)
    to_date = models.DateField('To Date', null=True, blank=True)
    agency = models.ForeignKey('Agency', on_delete=models.CASCADE, related_name='agency')
    photo_index_only = models.BooleanField('Photo Index Only', default=False)
    public = models.BooleanField('Public', default=True)
    fully_scanned = models.BooleanField('Fully Scanned', default=False)
    remarks = models.TextField(null=True, blank=True)
    index_service_url = models.URLField('Index Service URL', max_length=256, null=True, blank=True)
    frames_service_url = models.URLField('Frames Service URL', max_length=256, null=True, blank=True)
    mosaic_service_url = models.URLField('Mosaic Service URL', max_length=256, null=True, blank=True)
    ls4_link = models.CharField(max_length=200, null=True, blank=True)
    qr_code_url = models.URLField('QR Code URL', max_length=256, null=True, blank=True)
    number_of_boxes = models.PositiveIntegerField('Number of Boxes', null=True, blank=True)
    thumbnail_image = models.TextField(
        'Thumb Image',
        max_length=200,
        null=True,
        blank=True,
        default='https://s3.amazonaws.com/data.tnris.org/historical_images/historical_thumbnail.jpg'
    )
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def delete_s3_files(self):
        # do that boto dance
        client = boto3.client('s3')
        # set aside list for compiling keys
        key_list = []
        # list Objects
        collection_prefix = str(self.id) + '/assets'
        response = client.list_objects_v2(
            Bucket='data.tnris.org',
            Prefix=collection_prefix
        )

        if 'Contents' in response.keys():
            # add image keys to list
            for image in response['Contents']:
                key_list.append({'Key':image['Key']})

            response = client.delete_objects(
                Bucket='data.tnris.org',
                Delete={'Objects': key_list}
            )
            print('%s s3 files: delete success!' % self.collection)
        return

    # overwrite default model delete method so that all associated
    # s3 files get deleted as well
    def delete(self, *args, **kwargs):
        self.delete_s3_files()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.collection


class Image(models.Model):
    """
    Defines available image resources.
    Related to :model:`lore.collection`.
    """

    class Meta:
        db_table = 'historical_image'
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    image_id = models.UUIDField(
        'Image ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    collection_id = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        on_delete=models.CASCADE,
        related_name='image_collections'
    )
    image_url = models.URLField(
        'Image URL',
        max_length=255
    )
    caption = models.CharField(
        'Image Caption',
        max_length=255,
        null=True,
        blank=True
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
        print(key)
        response = client.delete_object(
            Bucket='data.tnris.org',
            Key=key
        )
        print(self)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.image_url.replace('https://s3.amazonaws.com/data.tnris.org/', 'https://data.geographic.texas.gov/')


"""
********** Database Views **********
**** Used as the API endpoints ****
"""

class ChcView(models.Model):
    """
    Compiled Historical Collection view presents Collection table with all
    associated relates joined
    """

    class Meta:
        managed = False
        db_table = "compiled_historical_collection"
        verbose_name = 'Compiled Historical Collection'
        verbose_name_plural = 'Compiled Historical Collections'

    collection_id = models.UUIDField(
        'Historical Collection ID',
        primary_key=True
    )
    collection = models.CharField(
        'Collection',
        max_length=24
    )
    from_date = models.DateField(
        'From Date'
    )
    acquisition_date = models.DateField(
        'To Date (Acquisition)'
    )
    photo_index_only = models.BooleanField(
        'Photo Index Only'
    )
    public = models.BooleanField(
        'Public'
    )
    fully_scanned = models.BooleanField(
        'Fully Scanned'
    )
    index_service_url = models.CharField(
        'Index Service URL',
        max_length=256
    )
    frames_service_url = models.CharField(
        'Frames Service URL',
        max_length=256
    )
    mosaic_service_url = models.CharField(
        'Mosaic Service URL',
        max_length=256
    )
    counties = models.TextField(
        'Counties'
    )
    source_name = models.CharField(
        'Source Name',
        max_length=254
    )
    source_abbreviation = models.CharField(
        'Source Abbreviation',
        max_length=20
    )
    license_name = models.TextField(
        'License Name'
    )
    license_abbreviation = models.TextField(
        'License Abbreviation'
    )
    license_url = models.CharField(
        'License URL',
        max_length=255
    )
    images = models.TextField(
        'Sample Image URL'
    )
    products = models.TextField(
        'Products'
    )
    name = models.CharField(
        'Display Name',
        max_length=100
    )
    template = models.CharField(
        'Display Template',
        max_length=20
    )
    availability  = models.TextField(
        'Availability'
    )
    thumbnail_image = models.URLField(
        'Thumbnail Image URL'
    )
    category = models.TextField(
        'Category'
    )
    recommended_use = models.TextField(
        'Recommended Use'
    )
    scanned_index_ls4_links = models.TextField(
        'Scanned Index LS4 Links'
    )
    media_type = models.TextField(
        'Media Type'
    )
    general_scale = models.TextField(
        'General Scale'
    )
    about = models.TextField(
        'About'
    )

    def __str__(self):
        return self.name + str(self.to_date)
