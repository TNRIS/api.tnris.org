from django.db import models
from datetime import datetime
import uuid

"""
*************************** EMAIL TEMPLATES ****************************
********* USED TO FORMAT EMAILS SENT B/C OF FORM SUBMISSIONS ***********
"""


class EmailTemplate(models.Model):
    """Text template used as submitted form email body"""

    class Meta:
        db_table = 'contact_email_template'
        verbose_name = 'Email Template'
        verbose_name_plural = 'Email Templates'

    email_template_id = models.UUIDField(
        'Email Template ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email_template_type = models.CharField(
        'Email Template Type',
        max_length=50,
        null=False,
        blank=False
    )
    email_template_subject = models.CharField(
        'Email Template Subject',
        max_length=100,
        null=False,
        blank=False
    )
    email_template_body = models.TextField(
        'Email Template Body',
        null=False,
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
        return self.email_template_type


"""
*********************** FORM SUBMISSION TABLES *************************
"""


class GeneralContact(models.Model):
    """General Contact form on tnris.org"""

    class Meta:
        db_table = 'contact_general'
        verbose_name = 'General Question or Comment'
        verbose_name_plural = 'General Questions or Comments'

    general_contact_id = models.UUIDField(
        'General Contact ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    question_or_comments = models.TextField(
        'Question or Comment',
        null=False,
        blank=False
    )
    name = models.CharField(
        'Name',
        max_length=150,
        null=False,
        blank=False
    )
    email = models.CharField(
        'Email',
        max_length=150,
        null=False,
        blank=False
    )
    phone = models.CharField(
        'Phone',
        max_length=20,
        null=True,
        blank=True
    )
    address = models.CharField(
        'Address',
        max_length=150,
        null=True,
        blank=True
    )
    organization = models.CharField(
        'Organization',
        max_length=20,
        null=True,
        blank=True
    )
    industry = models.CharField(
        'Industry',
        max_length=50,
        null=True,
        blank=True
    )
    industry_other = models.CharField(
        'Industry (Other)',
        max_length=50,
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
        return self.name + " " + self.created.strftime('%Y-%m-%d %H:%M')
