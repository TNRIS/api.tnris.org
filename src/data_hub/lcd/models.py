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
    area_type = models.CharField(
        'Area Type',
        max_length=20,
        choices=AREA_TYPE_CHOICES
    )
    area_type_name = models.CharField(
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
    band_name = models.CharField(
        'Band Name',
        max_length=100,
        unique=True
    )
    band_abbreviation = models.CharField(
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
    category = models.CharField(
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
    data_type = models.CharField(
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
        return self.epsg_code


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
    file_type = models.CharField(
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
    license_abbreviation = models.CharField(
        'License Abbreviation',
        max_length=100
    )
    license_name = models.CharField(
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
    resolution = models.CharField(
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
    source_name = models.CharField(
        'Source Name',
        max_length=100,
        null=True,
        blank=True
    )
    source_abbreviation = models.CharField(
        'Source Abbreviation',
        max_length=10
    )
    source_website = models.URLField(
        'Source Website',
        max_length=255,
        null=True,
        blank=True
    )
    source_contact = models.CharField(
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
    template = models.CharField(
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
    use_type = models.CharField(
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


# """
# ********** Spatial Domain Tables **********
# """
#
# class StateType(models.Model):
#     """US and Mexican States domain table"""
#
#     class Meta:
#         db_table = 'state_type'
#         verbose_name = 'State'
#         verbose_name_plural = 'States'
#         unique_together = (
#             'state_fips',
#             'state_name'
#         )
#
#     state_type_id = models.UUIDField(
#         'State Type ID',
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )
#     state_fips = models.PositiveIntegerField(
#         'State FIPS',
#         null=True
#     )
#     state_name = models.CharField(
#         'State Name',
#         max_length=25
#     )
#     created = models.DateTimeField(
#         'Created',
#         auto_now_add=True
#     )
#     last_modified = models.DateTimeField(
#         'Last Modified',
#         auto_now=True
#     )
#
#     def __str__(self):
#         return self.state_name
#
#
# class CountyType(models.Model):
#     """Texas Counties domain table"""
#
#     class Meta:
#         db_table = 'county_type'
#         verbose_name = 'County'
#         verbose_name_plural = 'Counties'
#         unique_together = (
#             'county_fips',
#             'county_name'
#         )
#
#     county_type_id = models.UUIDField(
#         'County Type ID',
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )
#     county_fips = models.PositiveIntegerField(
#         'County FIPS',
#         unique=True
#     )
#     county_name = models.CharField(
#         'County Name',
#         max_length=20,
#         unique=True
#     )
#     created = models.DateTimeField(
#         'Created',
#         auto_now_add=True
#     )
#     last_modified = models.DateTimeField(
#         'Last Modified',
#         auto_now=True
#     )
#
#     def __str__(self):
#         return self.county_name
#
#
# class QuadType(models.Model):
#     """Texas USGS Quad domain table"""
#
#     class Meta:
#         db_table = 'quad_type'
#         verbose_name = 'Quad'
#         verbose_name_plural = 'Quads'
#         unique_together = (
#             'quad_id',
#             'quad_name'
#         )
#
#     quad_type_id = models.UUIDField(
#         'Quad Type ID',
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )
#     quad_id = models.PositiveIntegerField(
#         'USGS Quad ID',
#         unique=True
#     )
#     quad_name = models.CharField(
#         'USGS Quad Name',
#         max_length=50
#     )
#     created = models.DateTimeField(
#         'Created',
#         auto_now_add=True
#     )
#     last_modified = models.DateTimeField(
#         'Last Modified',
#         auto_now=True
#     )
#
#     def __str__(self):
#         return self.quad_name
#
#
# class QQuadType(models.Model):
#     """Texas USGS QQuad domain table"""
#
#     class Meta:
#         db_table = 'q_quad_type'
#         verbose_name = 'QQuad'
#         verbose_name_plural = 'QQuads'
#         unique_together = (
#             'q_quad_id',
#             'q_quad_name',
#             'quad_name'
#         )
#
#     q_quad_type_id = models.UUIDField(
#         'QQuad Type ID',
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )
#     q_quad_id = models.PositiveIntegerField(
#         'USGS QQuad ID',
#         unique=True
#     )
#     q_quad_name = models.CharField(
#         'USGS QQuad Name',
#         max_length=50
#     )
#     quad_name = models.CharField(
#         'USGS Quad Name',
#         max_length=50
#     )
#     created = models.DateTimeField(
#         'Created',
#         auto_now_add=True
#     )
#     last_modified = models.DateTimeField(
#         'Last Modified',
#         auto_now=True
#     )
#
#     def __str__(self):
#         return self.q_quad_name
#
#
# class UsngType(models.Model):
#     """Texas US National Grid domain table"""
#
#     class Meta:
#         db_table = 'usng_type'
#         verbose_name = 'US National Grid'
#         verbose_name_plural = 'US National Grids'
#         unique_together = (
#             'northing',
#             'easting',
#             'utm_grid_zone',
#             'grid_100k',
#             'usng_name'
#         )
#
#     usng_type_id = models.UUIDField(
#         'USNG 1000 Type ID',
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )
#     northing = models.PositiveIntegerField(
#         'Northing'
#     )
#     easting = models.PositiveIntegerField(
#         'Easting'
#     )
#     utm_grid_zone = models.CharField(
#         'UTM Grid Zone',
#         max_length=4
#     )
#     grid_100k = models.CharField(
#         '100000 Meter Square',
#         max_length=2
#     )
#     usng_name = models.CharField(
#         'USNG Name',
#         max_length=16,
#         unique=True
#     )
#     created = models.DateTimeField(
#         'Created',
#         auto_now_add=True
#     )
#     last_modified = models.DateTimeField(
#         'Last Modified',
#         auto_now=True
#     )
#
#     def __str__(self):
#         return self.usng_name


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
        verbose_name = 'Band'
        verbose_name_plural = 'Bands'

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
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
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
        verbose_name = 'Data Type'
        verbose_name_plural = 'Data Types'
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
        verbose_name = 'EPSG Code'
        verbose_name_plural = 'EPSG Codes'
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
        verbose_name = 'File Type'
        verbose_name_plural = 'File Types'
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
        verbose_name = 'Resolution'
        verbose_name_plural = 'Resolutions'
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
        verbose_name = 'Use'
        verbose_name_plural = 'Uses'
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


# """
# ********** Spatial Lookup Tables **********
# """
#
# class StateResource(models.Model):
#     """
#     Defines the state a downloadable resource intersects.
#     Related to :model:`lcd.state_type` and :model:`lcd.resource`.
#     """
#
#     class Meta:
#         db_table = 'state_resource'
#         verbose_name = 'State Resource'
#         verbose_name_plural = 'State Resources'
#
#     state_resource_id = models.UUIDField(
#         'State Resource ID',
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )
#     state_type_id = models.ForeignKey(
#         'StateType',
#         db_column='state_type_id',
#         on_delete=models.CASCADE,
#         related_name='state_types'
#     )
#     resource_id = models.ForeignKey(
#         'Resource',
#         db_column='resource_id',
#         on_delete=models.CASCADE,
#         related_name='resources'
#     )
#     created = models.DateTimeField(
#         'Created',
#         auto_now_add=True
#     )
#     last_modified = models.DateTimeField(
#         'Last Modified',
#         auto_now=True
#
#     def __str__(self):
#         return self.state_type_id.state_name
#
#
# class CountyResource(models.Model):
#     """
#     Defines the county a downloadable resource intersects.
#     Related to :model:`lcd.county_type` and :model:`lcd.resource`.
#     """
#
#     class Meta:
#         db_table = 'county_resource'
#         verbose_name = 'County Resource'
#         verbose_name_plural = 'County Resources'
#
#     county_resource_id = models.UUIDField(
#         'County Resource ID',
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )
#     county_type_id = models.ForeignKey(
#         'CountyType',
#         db_column='county_type_id',
#         on_delete=models.CASCADE,
#         related_name='county_types'
#     )
#     resource_id = models.ForeignKey(
#         'Resource',
#         db_column='resource_id',
#         on_delete=models.CASCADE,
#         related_name='resources'
#     )
#     created = models.DateTimeField(
#         'Created',
#         auto_now_add=True
#     )
#     last_modified = models.DateTimeField(
#         'Last Modified',
#         auto_now=True
#
#     def __str__(self):
#         return self.county_type_id.county_name
#
#
# class QuadResource(models.Model):
#     """
#     Defines the USGS quad a downloadable resource intersects.
#     Related to :model:`lcd.quad_type` and :model:`lcd.resource`.
#     """
#
#     class Meta:
#         db_table = 'quad_resource'
#         verbose_name = 'Quad Resource'
#         verbose_name_plural = 'Quad Resources'
#
#     quad_resource_id = models.UUIDField(
#         'Quad Resource ID',
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )
#     quad_type_id = models.ForeignKey(
#         'QuadType',
#         db_column='quad_type_id',
#         on_delete=models.CASCADE,
#         related_name='quad_types'
#     )
#     resource_id = models.ForeignKey(
#         'Resource',
#         db_column='resource_id',
#         on_delete=models.CASCADE,
#         related_name='resources'
#     )
#     created = models.DateTimeField(
#         'Created',
#         auto_now_add=True
#     )
#     last_modified = models.DateTimeField(
#         'Last Modified',
#         auto_now=True
#
#     def __str__(self):
#         return self.quad_type_id.quad_name
#
#
# class QQuadResource(models.Model):
#     """
#     Defines the USGS qquad a downloadable resource intersects.
#     Related to :model:`lcd.q_quad_type` and :model:'resource'.
#     """
#
#     class Meta:
#         db_table = 'q_quad_resource'
#         verbose_name = 'QQuad Resource'
#         verbose_name_plural = 'QQuad Resources'
#
#     q_quad_resource_id = models.UUIDField(
#         'QQuad Resource ID',
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )
#     q_quad_type_id = models.ForeignKey(
#         'QQuadType',
#         db_column='q_quad_type_id',
#         on_delete=models.CASCADE,
#         related_name='q_quad_types'
#     )
#     resource_id = models.ForeignKey(
#         'Resource',
#         db_column='resource_id',
#         on_delete=models.CASCADE,
#         related_name='resources'
#     )
#     created = models.DateTimeField(
#         'Created',
#         auto_now_add=True
#     )
#     last_modified = models.DateTimeField(
#         'Last Modified',
#         auto_now=True
#
#     def __str__(self):
#         return self.q_quad_type_id.q_quad_name
#
#
# class UsngResource(models.Model):
#     """
#     Defines the US National Grid a downloadable resource intersects.
#     Related to :model:`lcd.usng_type` and :model:`lcd.resource`.
#     """
#
#     class Meta:
#         db_table = 'usng_resource'
#         verbose_name = 'USNG Resource'
#         verbose_name_plural = 'USNG Resources'
#
#     usng_resource_id = models.UUIDField(
#         'USNG Resource ID',
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )
#     usng_type_id = models.ForeignKey(
#         'UsngType',
#         db_column='usng_type_id',
#         on_delete=models.CASCADE,
#         related_name='usng_types'
#     )
#     resource_id = models.ForeignKey(
#         'Resource',
#         db_column='resource_id',
#         on_delete=models.CASCADE,
#         related_name='resources'
#     )
#     created = models.DateTimeField(
#         'Created',
#         auto_now_add=True
#     )
#     last_modified = models.DateTimeField(
#         'Last Modified',
#         auto_now=True
#
#     def __str__(self):
#         return self.usng_type_id.usng_name


"""
********** Primary Tables **********
"""

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
    resource_type = models.CharField(
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


class Collection(models.Model):
    """
    Defines collections in the data catalog.
    """

    class Meta:
        db_table = 'collection'
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'

    collection_id = models.UUIDField(
        'Collection ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    display_name = models.CharField(
        'Display Name',
        max_length=200
    )
    acquisition_date = models.DateField(
        'Acquisiiton Date',
        null=True,
        blank=True
    )
    short_description = models.CharField(
        'Short Description',
        
    )
