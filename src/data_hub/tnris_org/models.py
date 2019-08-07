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
    """Regular training courses scheduled by Tnris"""

    class Meta:
        db_table = 'tnris_training'
        verbose_name = 'Tnris Training'
        verbose_name_plural = 'Tnris Trainings'

    training_id = models.UUIDField(
        'Training ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        blank=False
    )
    start_date_time = models.DateTimeField(
        'Training Start Date & Time',
        blank=False
    )
    end_date_time = models.DateTimeField(
        'Training End Date & Time',
        blank=False
    )
    title = models.CharField(
        'Training Title',
        max_length=255,
        blank=False
    )
    instructor = models.CharField(
        'Training Instructor',
        max_length=100,
        blank=False
    )
    cost = models.DecimalField(
        'Training Cost',
        max_digits=6,
        decimal_places=2,
        blank=False
    )
    registration_open = models.BooleanField(
        'Registration Open',
        default=False,
        null=False
    )
    public = models.BooleanField(
        'Public',
        default=False,
        null=False
    )
    description = models.TextField(
        'Training Description'
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        'Last Modified',
        auto_now=True
    )

    @property
    def year(self):
        return self.start_date_time.strftime("%Y")

    def __str__(self):
        return self.title


class TnrisForumTraining(models.Model):
    """Texas GIS Forum training courses scheduled by Tnris"""

    class Meta:
        db_table = 'tnris_forum_training'
        verbose_name = 'Tnris Forum Training'
        verbose_name_plural = 'Tnris Forum Trainings'

    training_id = models.UUIDField(
        'Training ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        blank=False
    )
    training_day = models.PositiveSmallIntegerField(
        'Forum Training Day',
        blank=False
    )
    title = models.CharField(
        'Training Title',
        max_length=255,
        blank=False
    )
    start_date_time = models.DateTimeField(
        'Training Start Date & Time',
        blank=False
    )
    end_date_time = models.DateTimeField(
        'Training End Date & Time',
        blank=False
    )
    training_instructor = models.ForeignKey(
        'TnrisInstructor',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    cost = models.DecimalField(
        'Training Cost',
        max_digits=6,
        decimal_places=2,
        blank=False
    )
    registration_open = models.BooleanField(
        'Registration Open',
        default=False,
        null=False
    )
    public = models.BooleanField(
        'Public',
        default=False,
        null=False
    )
    location = models.CharField(
        'Training Location',
        max_length=255,
        blank=False
    )
    room = models.CharField(
        'Training Room',
        max_length=255,
        blank=True
    )
    max_students = models.PositiveSmallIntegerField(
        'Max Student Amount',
        blank=True,
        null=True
    )
    description = models.TextField(
        'Training Description'
    )
    teaser = models.TextField(
        'Training Teaser',
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

    @property
    def year(self):
        return self.start_date_time.strftime("%Y")

    def __str__(self):
        return self.title


"""
********** Domain Tables **********
"""


class TnrisInstructor(models.Model):
    """Instructor domain table for TnrisForumTraining"""

    class Meta:
        db_table = 'tnris_instructor'
        verbose_name = 'Tnris Instructor'
        verbose_name_plural = 'Tnris Instructors'
        ordering = ['name']

    instructor_id = models.UUIDField(
        'Instructor ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        blank=False
    )
    name = models.CharField(
        'Instructor Name',
        max_length=100,
        blank=False
    )
    company = models.CharField(
        'Instructor Company',
        max_length=100,
        blank=True,
        null=True
    )
    bio = models.TextField(
        'Instructor Bio',
        blank=True,
        null=True
    )
    headshot = models.URLField(
        'Image URL',
        max_length=255,
        blank=True,
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
