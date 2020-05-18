from django.db import models

import uuid
import boto3
import os


"""
********** TNRIS.ORG Static File/Resource Tables (Images, Docs, Training, GIO Calendar) **********
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
    sgm_note = models.BooleanField(
        'Solutions Group Note',
        default=False,
        null=False
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
    training_link = models.URLField(
        'Training Course Registration Link',
        max_length=255,
        null=False
    )
    category = models.ForeignKey(
        'TrainingCategory',
        db_column='training_category',
        on_delete=models.CASCADE,
        related_name='category'
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

    @property
    def fiscal_year(self):
        # if class start date month is before sept, use same year for
        # fiscal year. otherwise, add 1 for 'next' year
        return self.start_date_time.year if self.start_date_time.month < 9 else self.start_date_time.year + 1

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


class TnrisGioCalendarEvent(models.Model):
    """GIO Calendar Events"""

    class Meta:
        db_table = 'tnris_gio_calendar_event'
        verbose_name = 'Tnris GIO Calendar Event'
        verbose_name_plural = 'Tnris GIO Calendar Events'

    id = models.UUIDField(
        'Event ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        blank=False
    )
    start_date = models.DateField(
        'Event Start Date',
        blank=False,
        null=False
    )
    end_date = models.DateField(
        'Event End Date',
        blank=True,
        null=True
    )
    start_time = models.TimeField(
        'Event Start Time',
        blank=True,
        null=True
    )
    end_time = models.TimeField(
        'Event End Time',
        blank=True,
        null=True
    )
    title = models.CharField(
        'Event Title',
        max_length=255,
        blank=False
    )
    short_description = models.CharField(
        'Short Description',
        max_length=255,
        blank=True,
        null=True
    )
    location = models.CharField(
        'Event Location',
        max_length=150,
        blank=True,
        null=True
    )
    street_address = models.CharField(
        'Street Address',
        max_length=150,
        blank=True,
        null=True
    )
    city = models.CharField(
        'City',
        max_length=50,
        blank=True,
        null=True
    )
    state = models.CharField(
        'State Abbreviation',
        max_length=2,
        blank=True,
        null=True
    )
    zipcode = models.CharField(
        'Zipcode',
        max_length=10,
        blank=True,
        null=True
    )
    event_url = models.URLField(
        'Event URL',
        max_length=255,
        blank=True,
        null=True
    )
    public = models.BooleanField(
        'Public',
        default=False,
        null=False,
        help_text="Display on website!"
    )
    community_meeting = models.BooleanField(
        'Community Meeting',
        default=False,
        null=False
    )
    community_meeting_agenda_url = models.URLField(
        'Community Meeting Agenda URL',
        max_length=255,
        blank=True,
        null=True
    )
    solutions_group_meeting = models.BooleanField(
        'Solutions Group Meeting',
        default=False,
        null=False
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
        return self.title


"""
********** Domain Tables **********
"""


class TnrisInstructorType(models.Model):
    """Instructor domain table for TnrisForumTraining"""

    class Meta:
        db_table = 'tnris_instructor_type'
        verbose_name = 'Tnris Instructor Type'
        verbose_name_plural = 'Tnris Instructor Types'
        ordering = ('name',)

    instructor_type_id = models.UUIDField(
        'Instructor Type ID',
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

    def __str__(self):
        return self.name


class TrainingCategory(models.Model):
    """Category domain table for TnrisTraining"""

    class Meta:
        db_table = 'tnris_training_category'
        verbose_name = 'Tnris Training Category'
        verbose_name_plural = 'Tnris Training Categories'
        ordering = ('training_category',)

    training_category_id = models.UUIDField(
        'Category ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        blank=False
    )
    training_category = models.CharField(
        'Category',
        max_length=100,
        blank=False
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
        return self.training_category


"""
********** Relate Tables **********
"""


class TnrisInstructorRelate(models.Model):
    """Relate table between TnrisForumTraining and TnrisInstructor tables"""

    class Meta:
        db_table = 'tnris_instructor_relate'
        verbose_name = 'Tnris Instructor Relate'
        verbose_name_plural = 'Tnris Instructor Relates'
        unique_together = (
            'instructor_relate_id',
            'training_relate_id'
        )

    id = models.UUIDField(
        'Relate Primary Key',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    instructor_relate_id = models.ForeignKey(
        'TnrisInstructorType',
        db_column='instructor_relate_id',
        on_delete=models.CASCADE,
        related_name='tnris_instructor_type_ids'
    )
    training_relate_id = models.ForeignKey(
        'TnrisForumTraining',
        db_column='training_relate_id',
        on_delete=models.CASCADE,
        related_name='tnris_forum_training_ids'
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        'Last Modified',
        auto_now=True
    )


"""
********** Database Views **********
**** Used for the joined/related API endpoint ****
"""

class CompleteForumTrainingView(models.Model):
  """
  Complete Forum Training view presents forum training records with related instructor domains included
  """

  class Meta:
      managed = False
      db_table = 'complete_forum_training'
      verbose_name = 'Complete Forum Training'
      verbose_name_plural = 'Complete Forum Trainings'

  training_id = models.UUIDField(
      'Training ID',
      primary_key=True
  )
  training_day = models.PositiveSmallIntegerField(
      'Forum Training Day'
  )
  title = models.CharField(
      'Training Title',
      max_length=255
  )
  start_date_time = models.DateTimeField(
      'Training Start Date & Time'
  )
  end_date_time = models.DateTimeField(
      'Training End Date & Time'
  )
  cost = models.DecimalField(
      'Training Cost',
      max_digits=6,
      decimal_places=2
  )
  registration_open = models.BooleanField(
      'Registration Open'
  )
  public = models.BooleanField(
      'Public'
  )
  location = models.CharField(
      'Training Location',
      max_length=255
  )
  room = models.CharField(
      'Training Room',
      max_length=255
  )
  max_students = models.PositiveSmallIntegerField(
      'Max Student Amount'
  )
  description = models.TextField(
      'Training Description'
  )
  teaser = models.TextField(
      'Training Teaser'
  )
  instructor_info = models.TextField(
      'Instructor Info'
  )

  @property
  def year(self):
      return self.start_date_time.strftime("%Y")

  def __str__(self):
      return str(self.training_id)
