from django.db import models
import uuid


"""
These tables might be used in future versions of this app.
They were saved here in case we need them.
"""


"""
********** Spatial Domain Tables **********
**********    Not used in V1     **********
"""

class StateType(models.Model):
    """US and Mexican States domain table"""

    class Meta:
        db_table = 'state_type'
        verbose_name = 'State'
        verbose_name_plural = 'States'
        unique_together = (
            'state_fips',
            'state_name'
        )

    state_type_id = models.UUIDField(
        'State Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    state_fips = models.PositiveIntegerField(
        'State FIPS',
        null=True
    )
    state_name = models.TextField(
        'State Name',
        max_length=25
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
        return self.state_name


class CountyType(models.Model):
    """Texas Counties domain table"""

    class Meta:
        db_table = 'county_type'
        verbose_name = 'County'
        verbose_name_plural = 'Counties'
        unique_together = (
            'county_fips',
            'county_name'
        )

    county_type_id = models.UUIDField(
        'County Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    county_fips = models.PositiveIntegerField(
        'County FIPS',
        unique=True
    )
    county_name = models.TextField(
        'County Name',
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
        return self.county_name


class QuadType(models.Model):
    """Texas USGS Quad domain table"""

    class Meta:
        db_table = 'quad_type'
        verbose_name = 'Quad'
        verbose_name_plural = 'Quads'
        unique_together = (
            'quad_id',
            'quad_name'
        )

    quad_type_id = models.UUIDField(
        'Quad Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    quad_id = models.PositiveIntegerField(
        'USGS Quad ID',
        unique=True
    )
    quad_name = models.TextField(
        'USGS Quad Name',
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
        return self.quad_name


class QQuadType(models.Model):
    """Texas USGS QQuad domain table"""

    class Meta:
        db_table = 'q_quad_type'
        verbose_name = 'QQuad'
        verbose_name_plural = 'QQuads'
        unique_together = (
            'q_quad_id',
            'q_quad_name',
            'quad_name'
        )

    q_quad_type_id = models.UUIDField(
        'QQuad Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    q_quad_id = models.PositiveIntegerField(
        'USGS QQuad ID',
        unique=True
    )
    q_quad_name = models.TextField(
        'USGS QQuad Name',
        max_length=50
    )
    quad_name = models.TextField(
        'USGS Quad Name',
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
        return self.q_quad_name


class UsngType(models.Model):
    """Texas US National Grid domain table"""

    class Meta:
        db_table = 'usng_type'
        verbose_name = 'US National Grid'
        verbose_name_plural = 'US National Grids'
        unique_together = (
            'northing',
            'easting',
            'utm_grid_zone',
            'grid_100k',
            'usng_name'
        )

    usng_type_id = models.UUIDField(
        'USNG 1000 Type ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    northing = models.PositiveIntegerField(
        'Northing'
    )
    easting = models.PositiveIntegerField(
        'Easting'
    )
    utm_grid_zone = models.TextField(
        'UTM Grid Zone',
        max_length=4
    )
    grid_100k = models.TextField(
        '100000 Meter Square',
        max_length=2
    )
    usng_name = models.TextField(
        'USNG Name',
        max_length=16,
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
        return self.usng_name


"""
********** Spatial Lookup Tables **********
**********    Not used in V1     **********
"""

class StateResource(models.Model):
    """
    Defines the state a downloadable resource intersects.
    Related to :model:`lcd.state_type` and :model:`lcd.resource`.
    """

    class Meta:
        db_table = 'state_resource'
        verbose_name = 'State Resource'
        verbose_name_plural = 'State Resources'

    state_resource_id = models.UUIDField(
        'State Resource ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    state_type_id = models.ForeignKey(
        'StateType',
        db_column='state_type_id',
        on_delete=models.CASCADE,
        related_name='state_types'
    )
    resource_id = models.ForeignKey(
        'Resource',
        db_column='resource_id',
        on_delete=models.CASCADE,
        related_name='resources'
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        'Last Modified',
        auto_now=True

    def __str__(self):
        return self.state_type_id.state_name


class CountyResource(models.Model):
    """
    Defines the county a downloadable resource intersects.
    Related to :model:`lcd.county_type` and :model:`lcd.resource`.
    """

    class Meta:
        db_table = 'county_resource'
        verbose_name = 'County Resource'
        verbose_name_plural = 'County Resources'

    county_resource_id = models.UUIDField(
        'County Resource ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    county_type_id = models.ForeignKey(
        'CountyType',
        db_column='county_type_id',
        on_delete=models.CASCADE,
        related_name='county_types'
    )
    resource_id = models.ForeignKey(
        'Resource',
        db_column='resource_id',
        on_delete=models.CASCADE,
        related_name='resources'
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        'Last Modified',
        auto_now=True

    def __str__(self):
        return self.county_type_id.county_name


class QuadResource(models.Model):
    """
    Defines the USGS quad a downloadable resource intersects.
    Related to :model:`lcd.quad_type` and :model:`lcd.resource`.
    """

    class Meta:
        db_table = 'quad_resource'
        verbose_name = 'Quad Resource'
        verbose_name_plural = 'Quad Resources'

    quad_resource_id = models.UUIDField(
        'Quad Resource ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    quad_type_id = models.ForeignKey(
        'QuadType',
        db_column='quad_type_id',
        on_delete=models.CASCADE,
        related_name='quad_types'
    )
    resource_id = models.ForeignKey(
        'Resource',
        db_column='resource_id',
        on_delete=models.CASCADE,
        related_name='resources'
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        'Last Modified',
        auto_now=True

    def __str__(self):
        return self.quad_type_id.quad_name


class QQuadResource(models.Model):
    """
    Defines the USGS qquad a downloadable resource intersects.
    Related to :model:`lcd.q_quad_type` and :model:'resource'.
    """

    class Meta:
        db_table = 'q_quad_resource'
        verbose_name = 'QQuad Resource'
        verbose_name_plural = 'QQuad Resources'

    q_quad_resource_id = models.UUIDField(
        'QQuad Resource ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    q_quad_type_id = models.ForeignKey(
        'QQuadType',
        db_column='q_quad_type_id',
        on_delete=models.CASCADE,
        related_name='q_quad_types'
    )
    resource_id = models.ForeignKey(
        'Resource',
        db_column='resource_id',
        on_delete=models.CASCADE,
        related_name='resources'
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        'Last Modified',
        auto_now=True

    def __str__(self):
        return self.q_quad_type_id.q_quad_name


class UsngResource(models.Model):
    """
    Defines the US National Grid a downloadable resource intersects.
    Related to :model:`lcd.usng_type` and :model:`lcd.resource`.
    """

    class Meta:
        db_table = 'usng_resource'
        verbose_name = 'USNG Resource'
        verbose_name_plural = 'USNG Resources'

    usng_resource_id = models.UUIDField(
        'USNG Resource ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    usng_type_id = models.ForeignKey(
        'UsngType',
        db_column='usng_type_id',
        on_delete=models.CASCADE,
        related_name='usng_types'
    )
    resource_id = models.ForeignKey(
        'Resource',
        db_column='resource_id',
        on_delete=models.CASCADE,
        related_name='resources'
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        'Last Modified',
        auto_now=True

    def __str__(self):
        return self.usng_type_id.usng_name
