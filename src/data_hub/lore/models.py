# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

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


class Scale(models.Model):
    """Domain defining allowable scale values"""

    class Meta:
        db_table = 'scale'
        verbose_name_plural = 'Scales'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scale = models.PositiveIntegerField('Scale', unique=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return str(self.scale)


class PhotoIndex(models.Model):
    """Defines historical imagery collection photo indexes"""

    class Meta:
        db_table = 'photo_index'
        verbose_name = 'Photo Index'
        verbose_name_plural = 'Photo Indexes'
        unique_together = ('collection', 'scale', 'number_of_frames',
                           'scanned', 'physical_location')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE)
    scale = models.ForeignKey('Scale', on_delete=models.CASCADE, null=True, blank=True)
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
        unique_together = ("collection", "scale", "frame_size",
                           "number_of_frames", "scanned", "medium",
                           "physical_location")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE,
                                   related_name='Products')
    scale = models.ForeignKey('Scale', on_delete=models.CASCADE)
    frame_size = models.ForeignKey('FrameSize', on_delete=models.CASCADE)
    COVERAGE_TYPE_CHOICE = (
        ('Full', 'Full'),
        ('Partial', 'Partial')
    )
    coverage = models.CharField('Coverage', max_length=7,
                                choices=COVERAGE_TYPE_CHOICE, default='Partial')
    number_of_frames = models.PositiveIntegerField('Number of Frames',
                                                   default=0)
    scanned = models.PositiveIntegerField('Scanned', default=0)

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
    public = models.BooleanField('Public', default=True)
    remarks = models.TextField(null=True, blank=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)
    index_service_url = models.URLField('Index Service URL', max_length=256, null=True, blank=True)
    frames_service_url = models.URLField('Frames Service URL', max_length=256, null=True, blank=True)
    mosaic_service_url = models.URLField('Mosaic Service URL', max_length=256, null=True, blank=True)
    ls4_link = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.collection

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
    public = models.BooleanField(
        'Public'
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
    agency_name = models.CharField(
        'Acquiring Agency Name',
        max_length=254
    )
    agency_abbreviation = models.CharField(
        'Acquiring Agency Abbreviation',
        max_length=20
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

    def __str__(self):
        return self.name + str(self.to_date)
