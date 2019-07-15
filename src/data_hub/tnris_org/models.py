from django.db import models

import uuid
import boto3
import os


"""
********** TNRIS.ORG Static File/Resource Tables (Images, Docs, Training) **********
"""


class TnrisImage(models.Model):
    """Tnris.org image resource table containing an S3 bucket url for each image"""

    class Meta:
        db_table = 'tnris_image'
        verbose_name = 'Tnris Image'
        verbose_name_plural = 'Tnris Images'

    image_id = models.UUIDField(
        'Image ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    image_name = models.CharField(
        'Image Name',
        max_length=200,
        editable=False
    )
    image_url = models.URLField(
        'Image URL',
        max_length=255
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
        key = str(self).replace('https://tnris-org-static.s3.amazonaws.com/', '')
        print(key, 'successfully deleted')
        response = client.delete_object(
            Bucket='tnris-org-static',
            Key=key
        )
        print(self)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.image_url


class TnrisDocument(models.Model):
    """Tnris.org document resource table containing an S3 bucket url for each document"""

    class Meta:
        db_table = 'tnris_document'
        verbose_name = 'Tnris Document'
        verbose_name_plural = 'Tnris Documents'

    document_id = models.UUIDField(
        'Document ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    document_name = models.CharField(
        'Document Name',
        max_length=200,
        editable=False
    )
    document_url = models.URLField(
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
    # delete s3 doc files
    def delete(self, *args, **kwargs):
        client = boto3.client('s3')
        key = str(self).replace('https://tnris-org-static.s3.amazonaws.com/', '')
        print(key, 'successfully deleted')
        response = client.delete_object(
            Bucket='tnris-org-static',
            Key=key
        )
        print(self)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.document_url


class TnrisTraining(models.Model):
    """Training courses scheduled and organized by Tnris"""

    class Meta:
        db_table = 'tnris_training'
        verbose_name = 'Tnris Training'
        verbose_name_plural = 'Tnris Trainings'

    training_id = models.UUIDField(
        'Training ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    from_date = models.DateField(
        'Training Start Date'
    )
    to_date = models.DateField(
        'Training End Date'
    )
    title = models.CharField(
        'Training Title',
        max_length=255
    )
    from_time = models.TimeField(
        'Training Start Time'
    )
    to_time = models.TimeField(
        'Training End Time'
    )
    instructor = models.CharField(
        'Training Instructor',
        max_length=255
    )
    cost = models.DecimalField(
        'Training Cost',
        max_digits=6,
        decimal_places=2
    )
    registration_open = models.BooleanField(
        'Registration Open',
        default=False,
        null=False
    )
    instructor_bio = models.TextField(
        'Training Instructor Bio'
    )
    description = models.TextField(
        'Training Description'
    )

    def __str__(self):
        return self.class_title


class TnrisForumTraining(models.Model):
    """Training courses scheduled and organized by Tnris specifically for the Texas GIS Forum"""

    class Meta:
        db_table = 'tnris_forum_training'
        verbose_name = 'Tnris Forum Training'
        verbose_name_plural = 'Tnris Forum Trainings'

    training_id = models.UUIDField(
        'Training ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    training_day = models.PositiveSmallIntegerField(
        'Training Day'
    )
    title = models.CharField(
        'Training Title',
        max_length=255
    )
    from_time = models.TimeField(
        'Training Start Time'
    )
    to_time = models.TimeField(
        'Training End Time'
    )
    location = models.CharField(
        'Training Location',
        max_length=255
    )
    instructor = models.CharField(
        'Training Instructor',
        max_length=255
    )
    cost = models.DecimalField(
        'Training Cost',
        max_digits=6,
        decimal_places=2
    )
    registration_open = models.BooleanField(
        'Registration Open',
        default=False,
        null=False
    )
    instructor_bio = models.TextField(
        'Training Instructor Bio'
    )
    description = models.TextField(
        'Training Description'
    )
    teaser = models.TextField(
        'Training Teaser'
    )
    room = models.CharField(
        'Training Room',
        max_length=255
    )
    max_students = models.PositiveSmallIntegerField(
        'Max Student Amount'
    )

    def __str__(self):
        return self.class_title
