from django.db import models

import uuid

from django.db import models


class ZippedByAreaType(models.Model):
    """Domain defining areas that resources are zipped up by"""

    class Meta:
        db_table = 'zipped_by_area_type'
        verbose_name = 'Zipped By Area Type'
        verbose_name_plural = 'Zipped By Area Types'
        unique_together = ('zipped_by_area_type', 'zipped_by_area_type_name')

    zipped_by_area_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ZIPPED_BY_AREA_TYPE_CHOICES = (
        ('state', 'state'),
        ('county', 'county'),
        ('quad', 'quad'),
        ('qquad', 'qquad'),
        ('natgrid', 'natgrid'),
    )
    zipped_by_area_type = models.CharField('Zipped By Area Type', max_length=20, choices=ZIPPED_BY_AREA_TYPE_CHOICES)
    zipped_by_area_type_name = models.CharField('Zipped By Area Name', max_length=50)
    orig_data_download_id = models.PositiveIntegerField('Original Data Download ID', null=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.zipped_by_area_type_name + ' ' + self.zipped_by_area_type


class StateType(models.Model):
    """US and Mexican States domain table"""

    class Meta:
        db_table = 'state_type'
        verbose_name = 'State'
        verbose_name_plural = 'States'
        unique_together = ('state_fips', 'state_name')

    state_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state_fips = models.PositiveIntegerField('State FIPS', null=True)
    state_name = models.CharField('State Name', max_length=25)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.state_name

class CountyType(models.Model):
    """Texas Counties domain table"""

    class Meta:
        db_table = 'county_type'
        verbose_name = 'County'
        verbose_name_plural = 'Counties'
        unique_together = ('county_fips', 'county_name')

    county_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    county_fips = models.PositiveIntegerField('County FIPS', unique=True)
    county_name = models.CharField('County Name', max_length=20, unique=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.county_name


class QuadType(models.Model):
    """Texas USGS Quad domain table"""

    class Meta:
        db_table = 'quad_type'
        verbose_name = 'Quad'
        verbose_name_plural = 'Quads'
        unique_together = ('usgs_doq_id', 'usgs_doq_name')

    quad_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usgs_doq_id = models.PositiveIntegerField('USGS DOQ ID', unique=True)
    usgs_doq_name = models.CharField('USGS DOQ Name', max_length=40)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.usgs_doq_name


class QQuadType(models.Model):
    """Texas USGS QQuad domain table"""

    class Meta:
        db_table = 'q_quad_type'
        verbose_name = 'QQuad'
        verbose_name_plural = 'QQuads'
        unique_together = ('q_quad_id', 'q_quad_name')

    q_quad_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    q_quad_id = models.PositiveSmallIntegerField('QQuad ID', unique=True)
    q_quad_name = models.CharField('QQuad Name', max_length=2)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.q_quad_name


class UsngType(models.Model):
    """Texas US National Grid 1000 domain table"""

    class Meta:
        db_table = 'usng_1000_type'
        verbose_name = 'US National Grid'
        verbose_name_plural = 'US National Grids'
        unique_together = ('utm_grid_zone', 'hk_meter_square', 'grid_coordinates')

    usng_1000_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utm_grid_zone = models.CharField('UTM Grid Zone', max_length=4)
    hk_meter_square = models.CharField('100000 Meter Square', max_length=2)
    grid_coordinates = models.PositiveIntegerField('Grid Coordinates')
    usng_name = models.CharField('USNG Name', max_length=16)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.usng_name


class TemplateType(models.Model):
    """HTML template domain table"""

    class Meta:
        db_table = 'template_type'
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'

    template_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.CharField('Template', max_length=100, unique=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.template


class LicenseType(models.Model):
    """Software license domain table"""

    class Meta:
        db_table = 'license_type'
        verbose_name = 'License'
        verbose_name_plural = 'Licenses'
        unique_together = ('license_abbreviation', 'license_name', 'license_url')

    license_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    license_abbreviation = models.CharField('License Abbreviation', max_length=100)
    license_name = models.CharField('License Name', max_length=200)
    license_url = models.URLField('License URL', max_length=200, null=True, blank=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.license_abbreviation


class UseType(models.Model):
    """Recommended data usage domain table"""

    class Meta:
        db_table = 'use_type'
        verbose_name = 'Use type'
        verbose_name_plural = 'Use Types'

    use_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    use_type = models.CharField('Use', max_length=100, unique=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.use_type


class FileType(models.Model):
    """Available file formats domain table"""

    class Meta:
        db_table = 'file_type'
        verbose_name = 'File Type'
        verbose_name_plural = 'File Types'

    file_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_type = models.CharField('File Type', max_length=25, unique=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.file_type


class DataType(models.Model):
    """Available data types domain table"""

    class Meta:
        db_table = 'data_type'
        verbose_name = 'Data Type'
        verbose_name_plural = 'Data Types'

    data_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_type = models.CharField('Data Type', max_length=20, unique=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.data_type


class ResolutionType(models.Model):
    """Available resolutions domain table"""

    class Meta:
        db_table = 'resolution_type'
        verbose_name = 'Resolution Type'
        verbose_name_plural = 'Resolution Types'

    resolution_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resolution = models.CharField('Resolution', max_length=20, unique=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.resolution


class EpsgType(models.Model):
    """EPSG spatial reference domain table"""

    class Meta:
        db_table = 'epsg_type'
        verbose_name = 'EPSG Type'
        verbose_name_plural = 'EPSG Types'

    epsg_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    epsg_code = models.PositiveIntegerField('EPSG Code', unique=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.epsg_code


class CategoryType(models.Model):
    """Data categories domain table"""

    class Meta:
        db_table = 'category_type'
        verbose_name = 'Category Type'
        verbose_name_plural = 'Category Types'

    category_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = resolution = models.CharField('Category', max_length=50, unique=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.category
