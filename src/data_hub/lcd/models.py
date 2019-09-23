from django.db import models

import uuid
import boto3
import os


"""
********** Domain Tables **********
"""


class AreaType(models.Model):
    """Domain table defining areas that resources intersect"""

    class Meta:
        db_table = 'area_type'
        verbose_name = 'Area Type'
        verbose_name_plural = 'Area Types'
        ordering = ('area_type', 'area_type_name',)
        unique_together = (
            'area_type',
            'area_code'
        )

    area_type_id = models.UUIDField(
        'Area Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    AREA_TYPE_CHOICES = (
        ('state', 'state'),
        ('county', 'county'),
        ('quad', 'quad'),
        ('qquad', 'qquad'),
        ('natgrid', 'natgrid'),
    )
    area_type = models.TextField(
        'Area Type',
        max_length=20,
        choices=AREA_TYPE_CHOICES
    )
    area_type_name = models.TextField(
        'Area Type Name',
        max_length=50
    )
    orig_data_download_id = models.PositiveIntegerField(
        'Original Data Download ID',
        null=True
    )
    area_code = models.TextField(
        'Area Code',
        max_length=11
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
        return self.area_type_name


class CategoryType(models.Model):
    """Data categories domain table"""

    class Meta:
        db_table = 'category_type'
        verbose_name = 'Category Type'
        verbose_name_plural = 'Category Types'

    category_type_id = models.UUIDField(
        'Category Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    category = models.TextField(
        'Category',
        max_length=50,
        unique=True
    )
    filter_name = models.TextField(
        'Filter Name',
        max_length=50
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
        return self.category


class EpsgType(models.Model):
    """EPSG spatial reference domain table"""

    class Meta:
        db_table = 'epsg_type'
        verbose_name = 'EPSG Type'
        verbose_name_plural = 'EPSG Types'

    epsg_type_id = models.UUIDField(
        'EPSG Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    epsg_code = models.PositiveIntegerField(
        'EPSG Code',
        unique=True
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
        return str(self.epsg_code)


class FileType(models.Model):
    """Available file formats domain table"""

    class Meta:
        db_table = 'file_type'
        verbose_name = 'File Type'
        verbose_name_plural = 'File Types'

    file_type_id = models.UUIDField(
        'File Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    file_type = models.TextField(
        'File Type',
        max_length=25,
        unique=True
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
        return self.file_type


class LicenseType(models.Model):
    """Software license domain table"""

    class Meta:
        db_table = 'license_type'
        verbose_name = 'License Type'
        verbose_name_plural = 'License Types'
        unique_together = (
            'license_abbreviation',
            'license_name',
            'license_url'
        )

    license_type_id = models.UUIDField(
        'License Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    license_abbreviation = models.TextField(
        'License Abbreviation',
        max_length=100
    )
    license_name = models.TextField(
        'License Name',
        max_length=200
    )
    license_url = models.URLField(
        'License URL',
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

    def __str__(self):
        return self.license_abbreviation


class ResolutionType(models.Model):
    """Available resolutions domain table"""

    class Meta:
        db_table = 'resolution_type'
        verbose_name = 'Resolution Type'
        verbose_name_plural = 'Resolution Types'

    resolution_type_id = models.UUIDField(
        'Resolution Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    resolution = models.TextField(
        'Resolution',
        max_length=20,
        unique=True
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
        return self.resolution


class ResourceType(models.Model):
    """Available resource download types domain table"""

    class Meta:
        db_table = 'resource_type'
        verbose_name = 'Resource Type'
        verbose_name_plural = 'Resource Types'
        ordering = ('resource_type_name',)

    unique_together = (
        'resource_type_id',
        'resource_type_name',
        'resource_type_abbreviation'
    )

    resource_type_id = models.UUIDField(
        'Resource Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    resource_type_name = models.TextField(
        'Resource Type Name',
        max_length=50,
        unique=True
    )
    resource_type_abbreviation = models.TextField(
        'Resource Type Abbreviation',
        max_length=10,
        unique=True
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
        return self.resource_type_name


class SourceType(models.Model):
    """Sources domain table"""

    class Meta:
        db_table = 'source_type'
        verbose_name = 'Source Type'
        verbose_name_plural = 'Source Types'
        unique_together = (
            'source_name',
            'source_abbreviation',
            'source_website',
            'source_contact'
        )

    source_type_id = models.UUIDField(
        'Source Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    source_name = models.TextField(
        'Source Name',
        max_length=100
    )
    source_abbreviation = models.TextField(
        'Source Abbreviation',
        max_length=100,
        null=True,
        blank=True
    )
    source_website = models.URLField(
        'Source Website',
        max_length=255,
        null=True,
        blank=True
    )
    source_data_website = models.URLField(
        'Source Data Website',
        max_length=255,
        null=True,
        blank=True
    )
    source_contact = models.TextField(
        'Source Contact',
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

    def __str__(self):
        return "%s (%s)" % (self.source_name, self.source_abbreviation)


class TemplateType(models.Model):
    """HTML template domain table"""

    class Meta:
        db_table = 'template_type'
        verbose_name = 'Template Type'
        verbose_name_plural = 'Template Types'

    template_type_id = models.UUIDField(
        'Template Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    template = models.TextField(
        'Template',
        max_length=100,
        unique=True
    )
    filter_name = models.TextField(
        'Filter Name',
        max_length=50
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
        return self.template


class UseType(models.Model):
    """Recommended data usage domain table"""

    class Meta:
        db_table = 'use_type'
        verbose_name = 'Use type'
        verbose_name_plural = 'Use Types'

    use_type_id = models.UUIDField(
        'Use Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    use_type = models.TextField(
        'Use',
        max_length=100,
        unique=True
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
        return self.use_type


"""
********** Lookup Tables **********
"""


class CategoryRelate(models.Model):
    """
    Defines categories that a collection in the data catalog is associated with.
    Related to :model:`lcd.category_type` and :model:`lcd.collection`.
    """

    class Meta:
        db_table = 'category_relate'
        verbose_name = 'Category Lookup'
        verbose_name_plural = 'Category Lookups'
        unique_together = (
            'category_type_id',
            'collection_id'
        )

    category_relate_id = models.UUIDField(
        'Category Relate ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    category_type_id = models.ForeignKey(
        'CategoryType',
        db_column='category_type_id',
        on_delete=models.CASCADE,
        related_name='category_types'
    )
    collection_id = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        on_delete=models.CASCADE,
        related_name='category_collections'
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
        return self.category_type_id.category


class CountyRelate(models.Model):
    """Defines which county a collection has coverage for
    """

    class Meta:
        db_table = 'collection_county_relate'
        verbose_name_plural = 'County Relate'
        unique_together = ("collection_id", "area_type_id")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection_id = models.ForeignKey('Collection', db_column='collection_id', on_delete=models.CASCADE, related_name='Collections')
    area_type_id = models.ForeignKey('AreaType', db_column='area_type_id', on_delete=models.CASCADE, related_name='AreaType')
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.area_type.area_type_name


class EpsgRelate(models.Model):
    """
    Defines the spatial references for collections in the data catalog.
    Related to :model;`lcd.epsg_type` and :model:`lcd.collection`.
    """

    class Meta:
        db_table = 'epsg_relate'
        verbose_name = 'EPSG Code Lookup'
        verbose_name_plural = 'EPSG Type Lookups'
        unique_together = (
            'epsg_type_id',
            'collection_id'
        )

    epsg_relate_id = models.UUIDField(
        'EPSG Relate ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    epsg_type_id = models.ForeignKey(
        'EpsgType',
        db_column='epsg_type_id',
        on_delete=models.CASCADE,
        related_name='epsg_types'
    )
    collection_id = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        on_delete=models.CASCADE,
        related_name='epsg_collections'
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
        return str(self.epsg_type_id.epsg_code)


class FileTypeRelate(models.Model):
    """
    Defines the file types associated with collections in the data catalog.
    Related to :model:`lcd.file_type` and :model:`lcd.collection`.
    """

    class Meta:
        db_table = 'file_type_relate'
        verbose_name = 'File Type Lookup'
        verbose_name_plural = 'File Type Lookups'
        unique_together = (
            'file_type_id',
            'collection_id'
        )

    file_type_relate_id = models.UUIDField(
        'File Type Relate ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    file_type_id = models.ForeignKey(
        'FileType',
        db_column='file_type_id',
        on_delete=models.CASCADE,
        related_name='file_types'
    )
    collection_id = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        on_delete=models.CASCADE,
        related_name='file_type_collections'
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
        return self.file_type_id.file_type


class ResolutionRelate(models.Model):
    """
    Defines the resolutions for collections in the data catalog.
    Related to :model:`lcd.resolution_type` and :model:`lcd.collection`.
    """

    class Meta:
        db_table = 'resolution_relate'
        verbose_name = 'Resolution Lookup'
        verbose_name_plural = 'Resolution Lookups'
        unique_together = (
            'resolution_type_id',
            'collection_id'
        )

    resolution_relate_id = models.UUIDField(
        'Resolution Relate ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    resolution_type_id = models.ForeignKey(
        'ResolutionType',
        db_column='resolution_type_id',
        on_delete=models.CASCADE,
        related_name='resolution_types'
    )
    collection_id = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        on_delete=models.CASCADE,
        related_name='resolution_collections'
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
        return self.resolution_type_id.resolution


class ResourceTypeRelate(models.Model):
    """
    Defines the Resource Types for collections in the data catalog.
    Related to :model:`lcd.resource_type` and :model:`lcd.collection`.
    """

    class Meta:
        db_table = 'resource_type_relate'
        verbose_name = 'Resource Type Lookup'
        verbose_name_plural = 'Resource Type Lookups'
        unique_together = (
            'resource_type_id',
            'collection_id'
        )

    resource_type_relate_id = models.UUIDField(
        'Resource Type Relate ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    resource_type_id = models.ForeignKey(
        'ResourceType',
        db_column='resource_type_id',
        on_delete=models.CASCADE,
        related_name='resource_type'
    )
    collection_id = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        on_delete=models.CASCADE,
        related_name='resource_type_collections'
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
        return self.resource_type_id.resource_type_name


class UseRelate(models.Model):
    """
    Defines the reccommended uses for collections in the data catalog.
    Related to :model:`lcd.use_type` and :model:`lcd.collection`.
    """

    class Meta:
        db_table = 'use_relate'
        verbose_name = 'Use Lookup'
        verbose_name_plural = 'Use Lookups'
        unique_together = (
            'use_type_id',
            'collection_id'
        )

    use_relate_id = models.UUIDField(
        'Use Relate ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    use_type_id = models.ForeignKey(
        'UseType',
        db_column='use_type_id',
        on_delete=models.CASCADE,
        related_name='use_types'
    )
    collection_id = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        on_delete=models.CASCADE,
        related_name='use_collections'
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
        return self.use_type_id.use_type


"""
********** Primary Tables **********
"""

class Collection(models.Model):
    """
    Defines collections in the data catalog.
    Related to :model:`lcd.license_type`, :model:`lcd.source_type`,
    :model:`lcd.template_type`, and :model:`lcd.use_type`.
    """

    class Meta:
        db_table = 'collection'
        verbose_name = 'Dataset Collection'
        verbose_name_plural = 'Dataset Collections'
        ordering = ('name',)
        unique_together = (
            'name',
            'acquisition_date',
            'authoritative',
            'public',
            'known_issues',
            'md_filename',
            'wms_link',
            'popup_link',
            'carto_map_id',
            'thumbnail_image',
            'tile_index_url',
            'supplemental_report_url',
            'lidar_breaklines_url',
            'coverage_extent',
            'tags',
            'license_type_id',
            'source_type_id',
            'template_type_id'
        )

    collection_id = models.UUIDField(
        'Collection ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.TextField(
        'Name',
        max_length=200,
        null=True
    )
    acquisition_date = models.TextField(
        'Acquisition Date',
        max_length=200,
        null=True,
        blank=True
    )
    short_description = models.TextField(
        'Short Description',
        max_length=400,
        null=True,
        blank=True
    )
    description = models.TextField(
        'Description',
        null=True,
        blank=True
    )
    partners = models.TextField(
        'Partners',
        null=True,
        blank=True
    )
    authoritative = models.BooleanField(
        'Authoritative',
        default=False
    )
    public = models.BooleanField(
        'Public',
        default=False
    )
    known_issues = models.TextField(
        'Known Issues',
        null=True,
        blank=True
    )
    md_filename = models.TextField(
        'Markdown Filename',
        max_length=120,
        null=True,
        blank=True
    )
    wms_link = models.URLField(
        'WMS Link',
        max_length=255,
        null=True,
        blank=True
    )
    popup_link = models.URLField(
        'Popup Link',
        max_length=255,
        null=True,
        blank=True
    )
    carto_map_id = models.TextField(
        'Carto Map ID',
        max_length=100,
        null=True,
        blank=True
    )
    thumbnail_image = models.TextField(
        'Thumb Image',
        max_length=120,
        null=True,
        blank=True
    )
    tile_index_url = models.URLField(
        'Tile Index URL',
        max_length=255,
        null=True,
        blank=True
    )
    supplemental_report_url = models.URLField(
        'Supplemental Report URL',
        max_length=255,
        null=True,
        blank=True
    )
    lidar_breaklines_url = models.URLField(
        'Lidar Breaklines URL',
        max_length=255,
        null=True,
        blank=True
    )
    coverage_extent = models.TextField(
        'Coverage Extent',
        max_length=255,
        null=True,
        blank=True
    )
    tags = models.TextField(
        'Tags',
        null=True,
        blank=True
    )
    license_type_id = models.ForeignKey(
        'LicenseType',
        db_column='license_type_id',
        on_delete=models.CASCADE,
        related_name='license_types',
        null=True,
        blank=True
    )
    source_type_id = models.ForeignKey(
        'SourceType',
        db_column='source_type_id',
        on_delete=models.CASCADE,
        related_name='source_types',
        null=True,
        blank=True
    )
    template_type_id = models.ForeignKey(
        'TemplateType',
        db_column='template_type_id',
        on_delete=models.CASCADE,
        related_name='template_types',
        null=False,
        blank=False
    )
    esri_open_data_id = models.TextField(
        'ESRI Open Data ID',
        db_column='esri_open_data_id',
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

    def delete_s3_files(self):
        # do that boto dance
        client = boto3.client('s3')
        # set aside list for compiling keys
        key_list = []
        # list Objects
        collection_prefix = str(self.collection_id) + '/assets'
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
            print('%s s3 files: delete success!' % self.name)
        return

    # overwrite default model delete method so that all associated
    # s3 files get deleted as well
    def delete(self, *args, **kwargs):
        self.delete_s3_files()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Resource(models.Model):
    """
    Defines available resources.
    Related to :model:`lcd.area_type` and :model:`lcd.collection`.
    """

    class Meta:
        db_table = 'resource'
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'
        unique_together = (
            'resource_id',
            'resource',
            'area_type_id',
            'collection_id'
        )

    resource_id = models.UUIDField(

        'Resource ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    resource = models.URLField(
        'Resource URL',
        max_length=255
    )
    filesize = models.BigIntegerField(
        'Filesize',
        null=True,
        blank=True
    )
    area_type_id = models.ForeignKey(
        'AreaType',
        db_column='area_type_id',
        on_delete=models.CASCADE,
        related_name='area_types'
    )
    collection_id = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        on_delete=models.CASCADE,
        related_name='collections'
    )
    resource_type_id = models.ForeignKey(
        'ResourceType',
        db_column='resource_type_id',
        on_delete=models.CASCADE,
        related_name='resource_types'
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
        return self.resource


class Image(models.Model):
    """
    Defines available image resources.
    Related to :model:`lcd.collection`.
    """

    class Meta:
        db_table = 'image'
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
        return self.image_url


class OutsideEntityServices(models.Model):
    """
    Defines available outside entity services.
    Related to :model:`lcd.collection`.
    """

    class Meta:
        db_table = 'outside_entity_services'
        verbose_name = 'Outside Entity Service'
        verbose_name_plural = 'Outside Entity Services'

    service_id = models.UUIDField(
        'Service ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    collection_id = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        on_delete=models.CASCADE,
        related_name='outside_entity_service_collections'
    )
    service_name = models.TextField(
        'Service Name',
        db_column='service_name',
        null=False,
        blank=False
    )
    service_url = models.URLField(
        'Service URL',
        db_column='service_url',
        null=False,
        blank=False
    )


"""
********** Database Views **********
**** Used as the API endpoints ****
"""

class CcrView(models.Model):
    """
    Collection Catalog Records view presents Collection table with all
    associated relates joined
    """

    class Meta:
        managed = False
        db_table = "collection_catalog_record"
        verbose_name = 'Collection Catalog Record'
        verbose_name_plural = 'Cthumbollection Catalog Records'

    collection_id = models.UUIDField(
        'Collection ID',
        primary_key=True
    )
    name = models.TextField(
        'Name'
    )
    acquisition_date = models.TextField(
        'Acquisition Date'
    )
    short_description = models.TextField(
        'Short Description'
    )
    description = models.TextField(
        'Description'
    )
    partners = models.TextField(
        'Partners'
    )
    authoritative = models.BooleanField(
        'Authoritative'
    )
    public = models.BooleanField(
        'Public'
    )
    known_issues = models.TextField(
        'Known Issues'
    )
    wms_link = models.URLField(
        'WMS Link'
    )
    popup_link = models.URLField(
        'Popup Link'
    )
    carto_map_id = models.TextField(
        'Carto Map ID'
    )
    thumbnail_image = models.TextField(
        'Thumb Image'
    )
    images = models.TextField(
        'Image List'
    )
    tile_index_url = models.URLField(
        'Tile Index URL'
    )
    supplemental_report_url = models.URLField(
        'Supplemental Report URL'
    )
    lidar_breaklines_url = models.URLField(
        'Lidar Breaklines URL'
    )
    coverage_extent = models.TextField(
        'Coverage Extent'
    )
    tags = models.TextField(
        'Tags'
    )
    category = models.TextField(
        'Category'
    )
    spatial_reference = models.TextField(
        'Spatial Reference'
    )
    file_type = models.TextField(
        'File Type'
    )
    resolution = models.TextField(
        'Resolution'
    )
    recommended_use = models.TextField(
        'Recommended Use'
    )
    resource_types = models.TextField(
        'Resource Types'
    )
    data_types = models.TextField(
        'Data Types'
    )
    band_types = models.TextField(
        'Band Types'
    )
    source_name = models.TextField(
        'Source Name'
    )
    source_abbreviation = models.TextField(
        'Source Abbreviation'
    )
    source_website = models.CharField(
        'Source Website',
        max_length=255
    )
    source_data_website = models.CharField(
        'Source Website',
        max_length=255
    )
    source_contact = models.TextField(
        'Source Contact'
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
    template = models.TextField(
        'Template'
    )
    availability = models.TextField(
        'Availability'
    )
    counties = models.TextField(
        'Counties'
    )
    oe_service_names = models.TextField(
        'Outside Entity Service Names'
    )
    oe_service_urls = models.TextField(
        'Outside Entity Service URLs'
    )

    def __str__(self):
        return self.name


class RemView(models.Model):
    """
    Resource Management view presents Resource table with joins
    for Resource Type details
    """

    class Meta:
        managed = False
        db_table = "resource_management"
        verbose_name = 'Resource Management'
        verbose_name_plural = 'Resource Managements'

    resource_id = models.UUIDField(
        'Resource ID',
        primary_key=True
    )
    resource = models.CharField(
        'Resource URL',
        max_length=255
    )
    filesize = models.BigIntegerField(
        'Filesize',
        null=True,
        blank=True
    )
    area_type_id = models.UUIDField(
        'AreaType'
    )
    collection_id = models.UUIDField(
        'Collection'
    )
    resource_type_name = models.TextField(
        'Resource Type Name',
        max_length=50
    )
    resource_type_abbreviation = models.TextField(
        'Resource Type Abbreviation',
        max_length=10
    )
    area_type = models.TextField(
        'Area Type'
    )

    def __str__(self):
        return self.resource_id


class AreasView(models.Model):
  """
  Areas view presents resource table with aggregated collection_id
  """

  class Meta:
      managed = False
      db_table = "areas"
      verbose_name = 'Areas'
      verbose_name_plural = 'Areas'

  area_type_id = models.UUIDField(
      'Area Type ID',
      primary_key=True
  )
  area_type_name = models.TextField(
      'Area Type Name'
  )
  area_type = models.TextField(
      'Area Type'
  )
  download = models.TextField(
      'Download Collections'
  )
  historical = models.TextField(
      'Historical Collections'
  )
  outside_entity = models.TextField(
      'Outside Entity Collections'
  )
  order = models.TextField(
      'Order Collections'
  )
  collections = models.TextField(
      'All Collections Aggregated'
  )

  def __str__(self):
      return str(self.area_type_id)


"""
********** Dummy Models **********
**** Used for fake admin forms ****
"""

class XlargeSupplemental(models.Model):
    class Meta:
        verbose_name = 'X-Large Supplemental'
        verbose_name_plural = 'X-Large Supplementals'

    # placeholder for string representation applied at save of add form
    key = 'Xlarge Supplemental'

    def __str__(self):
        return self.key