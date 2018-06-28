from django.db import models

import uuid

from django.db import models


class ZippedByType(models.Model):
    """Domain defining areas that resources are zipped up by"""
    class Meta:
        db_table = 'zipped_by_type'
        verbose_name = 'Zipped By Type'
        verbose_name_plural = 'Zipped By Types'

    zipped_by_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ZIPPED_BY_AREA_CHOICES = (
        ('state', 'state'),
        ('county', 'county'),
        ('quad', 'quad'),
        ('qquad', 'qquad'),
        ('natgrid', 'natgrid'),
    )
    zipped_by_area = models.CharField('Zipped By Area', max_length=7, choices=ZIPPED_BY_AREA_CHOICES)
    zipped_by_area_name = models.CharField('Name', max_length=254, unique=True)
    abbreviation = models.CharField('Abbreviation', max_length=20, null=True,
                                    blank=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return ''
