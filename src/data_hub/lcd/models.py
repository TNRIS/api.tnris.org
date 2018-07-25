from django.db import models

import uuid

from django.db import models


"""
********** Domain Tables **********
"""

class AreaType(models.Model):
    """Domain table defining areas that resources intersect"""

    class Meta:
        db_table = 'area_type'
        verbose_name = 'Area Type'
        verbose_name_plural = 'Area Types'
        unique_together = (
            'area_type',
            'area_type_name'
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
    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        'Last Modified',
        auto_now=True
    )

    def __str__(self):
        return self.area_type_name + ' ' + self.area_type


class BandType(models.Model):
    """Available band types domain table"""

    class Meta:
        db_table = 'band_type'
        verbose_name = 'Band Type'
        verbose_name_plural = 'Band Types'
        unique_together = (
            'band_name',
            'band_abbreviation'
        )

    band_type_id = models.UUIDField(
        'Band Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    band_name = models.TextField(
        'Band Name',
        max_length=100,
        unique=True
    )
    band_abbreviation = models.TextField(
        'Band Abbreviation',
        max_length=10
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
        return self.band_abbreviation


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


class DataType(models.Model):
    """Available data types domain table"""

    class Meta:
        db_table = 'data_type'
        verbose_name = 'Data Type'
        verbose_name_plural = 'Data Types'

    data_type_id = models.UUIDField(
        'Data Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    data_type = models.TextField(
        'Data Type',
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
        return self.data_type


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


class SourceType(models.Model):
    """Data sources domain table"""

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
        return self.source_name


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

class BandRelate(models.Model):
    """
    Defines the spectral bands that a collection in the data catalog is associated with.
    Related to :model:`lcd.band_type` and :model:`lcd.collection`.
    """

    class Meta:
        db_table = 'band_relate'
        verbose_name = 'Band Lookup'
        verbose_name_plural = 'Band Lookups'

    band_relate_id = models.UUIDField(
        'Band Relate ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    band_type_id = models.ForeignKey(
        'BandType',
        db_column='band_type_id',
        on_delete=models.CASCADE,
        related_name='band_types'
    )
    collection_id = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        on_delete=models.CASCADE,
        related_name='band_collections'
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
        return self.band_type_id.band_abbreviation


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


class DataTypeRelate(models.Model):
    """
    Defines the data types associated with collections in the data catalog.
    Related to :model:`lcd.data_type` and :model:`lcd.collection`.
    """

    class Meta:
        db_table = 'data_type_relate'
        verbose_name = 'Data Type Lookup'
        verbose_name_plural = 'Data Type Lookups'
        unique_together = (
            'data_type_id',
            'collection_id'
        )

    data_type_relate_id = models.UUIDField(
        'Data Type Relate ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    data_type_id = models.ForeignKey(
        'DataType',
        db_column='data_type_id',
        on_delete=models.CASCADE,
        related_name='data_types'
    )
    collection_id = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        on_delete=models.CASCADE,
        related_name='data_type_collections'
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
        return self.data_type_id.data_type


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
        return self.epsg_type_id.epsg_code


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
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'
        unique_together = (
            'name',
            'acquisition_date',
            'short_description',
            'description',
            'authoritative',
            'public',
            'known_issues',
            'md_filename',
            'wms_link',
            'popup_link',
            'carto_map_id',
            'overview_image',
            'thumbnail_image',
            'natural_image',
            'urban_image',
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
    acquisition_date = models.DateField(
        'Acquisiiton Date',
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
    overview_image = models.TextField(
        'Overview Image',
        max_length=120,
        null=True,
        blank=True
    )
    thumbnail_image = models.TextField(
        'Thumb Image',
        max_length=120,
        null=True,
        blank=True
    )
    natural_image = models.TextField(
        'Natural Image',
        max_length=120,
        null=True,
        blank=True
    )
    urban_image = models.TextField(
        'Urban Image',
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
        db_column='Source_type_id',
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
        return self.display_name


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
            'resource_type',
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
    RESOURCE_TYPE_CHOICES = (
        ('download', 'download'),
        ('order', 'order'),
        ('website', 'website'),
    )
    resource_type = models.TextField(
        'Resource Type',
        max_length=20,
        choices=RESOURCE_TYPE_CHOICES
    )
    resource = models.URLField(
        'Resource URL',
        max_length=255
    )
    filesize = models.PositiveIntegerField(
        'Filesize'
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
