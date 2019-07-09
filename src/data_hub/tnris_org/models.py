from django.db import models

import uuid
import boto3
import os


"""
********** TNRIS.ORG Static File/Resource Tables (Images, Docs, Training) **********
"""


class TnrisImageUrl(models.Model):
    """Tnris.org image resource table containing an S3 bucket url for each image"""

    class Meta:
        db_table = 'tnris_image_url'
        verbose_name = 'Tnris Image Url'
        verbose_name_plural = 'Tnris Image Urls'

    image_id = models.UUIDField(
        'Image ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    image_url = models.URLField(
        'Image URL',
        max_length=255,
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
        key = str(self).replace('https://tnris-org-static.s3.amazonaws.com/images/', '')
        print(key)
        response = client.delete_object(
            Bucket='tnris-org-static',
            Key=key
        )
        print(self)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.image_url


class TnrisDocUrl(models.Model):
    """Tnris.org document resource table containing an S3 bucket url for each document"""

    class Meta:
        db_table = 'tnris_doc_url'
        verbose_name = 'Tnris Document Url'
        verbose_name_plural = 'Tnris Document Urls'

    doc_id = models.UUIDField(
        'Document ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    doc_url = models.URLField(
        'Document URL',
        max_length=255,
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
        key = str(self).replace('https://tnris-org-static.s3.amazonaws.com/documents/', '')
        print(key)
        response = client.delete_object(
            Bucket='tnris-org-static',
            Key=key
        )
        print(self)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.doc_url
