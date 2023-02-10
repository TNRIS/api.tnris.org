from django.db import models
from . import fields
from datetime import datetime
import uuid
from django_json_widget.widgets import JSONEditorWidget
from django import forms
from django.utils import timezone


    
class OrderDetailsType(models.Model):
    class Meta:
        db_table = 'order_details_type'
        verbose_name = 'Order Details Type'
        verbose_name_plural = 'Order DetailsTypes'
    
    details = fields.CryptoTextField(
        "Details",
        max_length=500000
    )

class OrderType(models.Model):
    """Store order information"""

    class Meta:
        db_table = 'order_type'
        verbose_name = 'Order Type'
        verbose_name_plural = 'Order Types'  
    
    id = models.UUIDField(
        'Order Id',
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    
    # Token for keeping track of a order form.
    order_token = models.UUIDField(
        'Order Token',
        editable=False,
        null=True,
        default=None
    )
    
    order_url = models.CharField(
        'Order url',
        editable=False,
        null=True,
        default=None,
        max_length=255
    )

    order_approved = models.BooleanField(
        'Order approved?',
        default=False,
        editable=True
    )
    
    received_receipt = models.BooleanField(
        'Receipt Received',
        editable=False,
        default=False,
        null=True,
        blank=True
    )
    
    tnris_notified = models.BooleanField(
        'TNRIS Notified?',
        editable=False,
        default=False,
        null=True,
        blank=True
    )
    
    customer_notified = models.BooleanField(
        'Customer Notified?',
        editable=False,
        default=False,
        null=True,
        blank=True
    )
    
    order_sent = models.BooleanField(
        'Order Sent?',
        editable=False,
        default=False,
        null=True,
        blank=True
    )
    
    approved_charge = models.CharField(
        "Approved Charge",
        editable=True,
        max_length=255,
        default="",
        null=True,
        blank=True
    )
    
    archived = models.BooleanField(
        'Order Archived?',
        default=False,
        editable=True
    )
    
    created = models.DateTimeField(
        'Created',
        default=timezone.now
    )
    
    last_modified = models.DateTimeField(
        'Last Modified',
        auto_now=True,
        editable=False
    )
    
    order_details = models.ForeignKey(
        OrderDetailsType,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return str(self.id)

    
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
        blank=False,
        help_text="Layman text/name of Form Submission table/model class."
    )
    form_id = models.CharField(
        'Form ID',
        max_length=40,
        null=False,
        blank=False,
        unique=True,
        help_text="'forum_id' value from form submission object."
    )
    sendpoint = models.CharField(
        'Sendpoint',
        max_length=20,
        null=False,
        blank=False,
        default='default',
        choices=[
            ('default', 'default'),
            ('email', 'email'),
            ('send_to_email', 'send_to_email')
        ],
        help_text="'default' to send to ticketing system. otherwise, form object key with email address to send to."
    )
    serializer_classname = models.CharField(
        'Serializer Classname',
        max_length=70,
        null=False,
        blank=False,
        unique=True,
        help_text="Serializer classname from serializers.py file. Must be exact. Typically is: '<-ModelClassname->Serializer'"
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
        blank=False,
        help_text="Form field values can be used by surrounding the database field name with double curly brackets. Ex: {{field_name}}",
        default="""A form has been submitted from: {{url}}
Form ID: {{form_id}}

Form parameters
==================
"""
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


class DataHubContact(models.Model):
    """
    DataHub contact form on data.tnris.org opened collection cards (Dataset Inquiry)
    https://data.tnris.org/collection/<<collection id>> (Contact Tab)
    """

    class Meta:
        db_table = 'contact_datahub'
        verbose_name = 'DataHub Question or Comment'
        verbose_name_plural = 'DataHub Questions or Comments'

    datahub_contact_id = models.UUIDField(
        'DataHub Contact ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        'Name',
        max_length=150,
        null=True,
        blank=True
    )
    email = models.CharField(
        'Email',
        max_length=150,
        null=True,
        blank=True
    )
    collection = models.CharField(
        'Collection Name',
        max_length=200,
        null=True,
        blank=True
    )
    uuid = models.UUIDField(
        'Collection UUID',
        null=True,
        blank=True
    )
    acquisition_date = models.CharField(
        'Acquisition Date',
        max_length=20,
        null=True,
        blank=True
    )
    category = models.CharField(
        'Category',
        max_length=350,
        null=True,
        blank=True
    )
    software = models.CharField(
        'Software',
        max_length=100,
        null=True,
        blank=True
    )
    message = models.TextField(
        'Question or Comment',
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


class DataHubOrder(models.Model):
    """
    DataHub order cart form on data.tnris.org (Dataset Order)
    https://data.tnris.org/cart/
    """

    class Meta:
        db_table = 'contact_datahub_order'
        verbose_name = 'DataHub Order'
        verbose_name_plural = 'DataHub Orders'

    datahub_order_id = models.UUIDField(
        'DataHub Order ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        'Name',
        max_length=150,
        null=True,
        blank=True
    )
    email = models.CharField(
        'Email',
        max_length=150,
        null=True,
        blank=True
    )
    phone = models.CharField(
        'Phone',
        max_length=20,
        null=True,
        blank=True
    )
    address = models.CharField(
        'Address',
        max_length=250,
        null=True,
        blank=True
    )
    organization = models.CharField(
        'Organization',
        max_length=60,
        null=True,
        blank=True
    )
    industry = models.CharField(
        'Industry',
        max_length=50,
        null=True,
        blank=True
    )
    harddrive = models.CharField(
        'Hard Drive',
        max_length=50,
        null=True,
        blank=True
    )
    delivery = models.CharField(
        'Delivery Method',
        max_length=50,
        null=True,
        blank=True
    )
    payment = models.CharField(
        'Payment',
        max_length=50,
        null=True,
        blank=True
    )
    notes = models.TextField(
        'Notes',
        null=True,
        blank=True
    )
    order = models.TextField(
        'Order',
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


class DataHubOutsideEntityContact(models.Model):
    """
    DataHub contact form on data.tnris.org outside entity cards (Outside Entity Data Inquiry)
    https://data.tnris.org/collection/<<collection id>> (Contact Tab)
    """

    class Meta:
        db_table = 'contact_datahub_outsideentity'
        verbose_name = 'DataHub Outside Entity Question or Comment'
        verbose_name_plural = 'DataHub Outside Entity Questions or Comments'

    datahub_outsideentity_id = models.UUIDField(
        'DataHub Outside Entity Contact ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        'Name',
        max_length=150,
        null=True,
        blank=True
    )
    email = models.CharField(
        'Email',
        max_length=150,
        null=True,
        blank=True
    )
    category = models.CharField(
        'Category',
        max_length=350,
        null=True,
        blank=True
    )
    software = models.CharField(
        'Software',
        max_length=100,
        null=True,
        blank=True
    )
    send_to_email = models.CharField(
        'Sent to Email',
        max_length=150,
        null=True,
        blank=True
    )
    send_to_name = models.CharField(
        'Sent to Name',
        max_length=150,
        null=True,
        blank=True
    )
    tnris_link = models.URLField(
        'TNRIS Outside Entity Card URL',
        max_length=360,
        null=True,
        blank=True
    )
    message = models.TextField(
        'Question or Comment',
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


class EducationContact(models.Model):
    """
    Education page Contact form on tnris.org
    https://tnris.org/education/
    """

    class Meta:
        db_table = 'contact_education'
        verbose_name = 'Education Question or Comment'
        verbose_name_plural = 'Education Questions or Comments'

    education_contact_id = models.UUIDField(
        'Education Contact ID',
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
        max_length=100,
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


class ForumJobBoardSubmission(models.Model):
    """
    Forum job board submission form on tnris.org forum pages
    https://tnris.org/texas-gis-forum/<<year>>/job-board
    """

    class Meta:
        db_table = 'contact_forumjobboard_submission'
        verbose_name = 'Forum Job Board Submission'
        verbose_name_plural = 'Forum Job Board Submissions'

    forumjobboard_submission_id = models.UUIDField(
        'Forum Job Board Submission ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
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
    organization = models.CharField(
        'Organization',
        max_length=20,
        null=True,
        blank=True
    )
    job_description_upload = models.URLField(
        'Job Description Upload URL',
        max_length=360,
        null=True,
        blank=True
    )
    other_notes = models.TextField(
        'Other Notes',
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

    @property
    def forum_year(self):
        return self.created.strftime("%Y")

    def __str__(self):
        return self.name + " " + self.created.strftime('%Y-%m-%d %H:%M')


class GeneralContact(models.Model):
    """
    General Contact form on tnris.org
    https://tnris.org/contact/
    """

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
        max_length=100,
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


class GeorodeoCallForPresentationsSubmission(models.Model):
    """
    Georodeo Call for Presentations submission form on tnris.org georodeo pages
    https://tnris.org/georodeo/call-for-presentations
    """

    class Meta:
        db_table = 'contact_georodeocallforpresentations_submission'
        verbose_name = 'Georodeo Call for Presentations Submission'
        verbose_name_plural = 'Georodeo Call for Presentations Submissions'

    georodeocallforpresentations_submission_id = models.UUIDField(
        'Georodeo Call for Presentations Submission ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        'Name',
        max_length=150,
        null=False,
        blank=False
    )
    organizationtitle = models.CharField(
        'Organization & Title',
        max_length=60,
        null=True,
        blank=True,
        help_text="Presenter organizaion name and position title"
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
    bio = models.TextField(
        'Presenter Bio',
        null=True,
        blank=True
    )
    category = models.CharField(
        'Category',
        max_length=100,
        null=True,
        blank=True
    )
    title = models.CharField(
        'Title',
        max_length=100,
        null=True,
        blank=True
    )
    description = models.TextField(
        'Description',
        null=True,
        blank=True
    )
    supplementallink = models.TextField(
        'Supplemental Link',
        null=True,
        blank=True
    )
    presenterheadshotphoto = models.URLField(
        'Presenter Headshot Photo URL',
        max_length=360,
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

    @property
    def georodeo_year(self):
        return self.created.strftime("%Y")

    def __str__(self):
        return self.name + " " + self.created.strftime('%Y-%m-%d %H:%M')


class GeorodeoRegistration(models.Model):
    """
    Georodeo Registration form on tnris.org georodeo pages
    https://tnris.org/georodeo/registration
    """

    class Meta:
        db_table = 'contact_georodeoregistration'
        verbose_name = 'Georodeo Registration'
        verbose_name_plural = 'Georodeo Registrations'

    georodeoregistration_id = models.UUIDField(
        'Georodeo Registration ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    firstname = models.CharField(
        'First Name',
        max_length=150,
        null=False,
        blank=False
    )
    lastname = models.CharField(
        'Last Name',
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
    organization = models.CharField(
        'Organization',
        max_length=60,
        null=True,
        blank=True
    )
    title = models.CharField(
        'Position Title',
        max_length=60,
        null=True,
        blank=True
    )
    vegetarian = models.CharField(
        'Vegetarian',
        max_length=3,
        null=True,
        blank=True,
        default='No',
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        help_text="Would you like to reserve a vegetarian lunch?"
    )
    attendingsocial = models.CharField(
        'Attending Social',
        max_length=3,
        null=True,
        blank=True,
        default='No',
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        help_text="Do you plan on attending the post-event social?"
    )
    tnrisemails = models.CharField(
        'TNRIS Emails',
        max_length=3,
        null=True,
        blank=True,
        default='No',
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        help_text="Would you like to receive emails from TNRIS related to future events?"
    )
    partneremails = models.CharField(
        'Partner Emails',
        max_length=3,
        null=True,
        blank=True,
        default='No',
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        help_text="Would you like to receive emails from sponsors and partners?"
    )
    previouslyattended = models.CharField(
        'Previously Attended',
        max_length=3,
        null=True,
        blank=True,
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        help_text="Have you ever attended the GeoRodeo before?"
    )
    experience = models.CharField(
        'Experience Level',
        max_length=60,
        null=True,
        blank=True,
        help_text="Non-Existent, Beginner, Intermediate, Kind of a Big Deal..., Elite Level Hacker, etc."
    )
    tools = models.TextField(
        'Tools',
        null=True,
        blank=True,
        help_text="What coding languages, tools, and/or libraries do you use?"
    )
    expectations = models.TextField(
        'Expectations',
        null=True,
        blank=True,
        help_text="What do you expect to hear about or learn at the GeoRodeo?"
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
    def georodeo_year(self):
        return self.created.strftime("%Y")

    def __str__(self):
        return self.firstname + " " + self.lastname + " " + self.created.strftime('%Y-%m-%d %H:%M')


class LakesOfTexasContact(models.Model):
    """
    Lakes of Texas app contact form on lake-gallery.tnris.org
    https://lake-gallery.tnris.org/about/#Contact
    """

    class Meta:
        db_table = 'contact_lakesoftexas'
        verbose_name = 'Lakes of Texas Question or Comment'
        verbose_name_plural = 'Lakes of Texas Questions or Comments'

    lakesoftexas_contact_id = models.UUIDField(
        'Lakes of Texas Contact ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        'Name',
        max_length=150,
        null=True,
        blank=True
    )
    email = models.CharField(
        'Email',
        max_length=150,
        null=True,
        blank=True
    )
    phone = models.CharField(
        'Phone',
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
    message = models.TextField(
        'Question or Comment',
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


class OrderMap(models.Model):
    """
    Order Map form on tnris.org
    https://tnris.org/order-map
    """

    class Meta:
        db_table = 'contact_ordermap'
        verbose_name = 'Map Order'
        verbose_name_plural = 'Map Orders'

    map_order_id = models.UUIDField(
        'Map Order ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    # Federal Print fields
    map_option = models.CharField(
        'Map Option',
        max_length=10,
        null=True,
        blank=True,
        choices=[
            ('USGS', 'USGS'),
            ('NWI', 'NWI'),
            ('FEMA', 'FEMA')
        ],
        help_text="For Federal Prints only."
    )
    map_description = models.TextField(
        'Map Description',
        null=True,
        blank=True,
        help_text="List all quads/panels and specify quantity for each map. For Federal Prints only."
    )
    # Pre-Made Map fields
    map_collection_name = models.CharField(
        'Map Collection Name',
        max_length=300,
        null=True,
        blank=True,
        help_text="For Pre-made Maps only."
    )
    map_sheet = models.CharField(
        'Map Sheet',
        max_length=300,
        null=True,
        blank=True,
        help_text="For Pre-made Maps only."
    )
    legislative_request = models.BooleanField(
        'Legislative Request?',
        default=False,
        help_text="For Pre-made Maps only."
    )
    # Custom Map Fields
    map_size = models.CharField(
        'Map Size',
        max_length=20,
        null=True,
        blank=True,
        choices=[
            ('8.5_by_11', '8.5_by_11'),
            ('11_by_17', '11_by_17'),
            ('24_by_24', '24_by_24'),
            ('24_by_28', '24_by_28'),
            ('30_by_30', '30_by_30'),
            ('36_by_36', '36_by_36'),
            ('60_by_60', '60_by_60'),
            ('custom_xlarge', 'custom_xlarge')
        ],
        help_text="For Custom Maps only."
    )
    custom_map_size = models.CharField(
        'Custom Map Size',
        max_length=100,
        null=True,
        blank=True,
        help_text="Custom sizes requests are only accepted for sizes greater than 60 x 60. For Custom Maps only."
    )
    map_scale = models.CharField(
        'Map Scale',
        max_length=100,
        null=True,
        blank=True,
        help_text="For Custom Maps only."
    )
    map_title = models.CharField(
        'Map Title',
        max_length=200,
        null=True,
        blank=True,
        help_text="For Custom Maps only."
    )
    map_date = models.CharField(
        'Map Date',
        max_length=100,
        null=True,
        blank=True,
        help_text="For Custom Maps only."
    )
    # General Info/Shared Fields
    type_of_data = models.CharField(
        'Type of Data',
        max_length=25,
        null=True,
        blank=True,
        default='Maps',
         choices=[
            ('N/A', 'N/A'),
            ('Maps', 'Maps')
        ]
    )
    type_of_map = models.CharField(
        'Type of Map',
        max_length=20,
        null=True,
        blank=True,
        choices=[
            ('Federal Print', 'Federal Print'),
            ('Pre-Made Print', 'Pre-Made Print'),
            ('Custom', 'Custom')
        ]
    )
    additional_info = models.TextField(
        'Additional Info',
        null=True,
        blank=True
    )
    name = models.CharField(
        'Name',
        max_length=150,
        null=True,
        blank=True
    )
    organization = models.CharField(
        'Organization',
        max_length=100,
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
    address_1 = models.CharField(
        'Address 1',
        max_length=150,
        null=True,
        blank=True
    )
    address_2 = models.CharField(
        'Address 2',
        max_length=150,
        null=True,
        blank=True
    )
    city = models.CharField(
        'City',
        max_length=75,
        null=True,
        blank=True
    )
    state = models.CharField(
        'State',
        max_length=50,
        null=True,
        blank=True
    )
    zip = models.CharField(
        'Zip',
        max_length=15,
        null=True,
        blank=True
    )
    email = models.CharField(
        'Email',
        max_length=150,
        null=True,
        blank=True
    )
    phone = models.CharField(
        'Phone',
        max_length=20,
        null=True,
        blank=True
    )
    fax = models.CharField(
        'Fax',
        max_length=20,
        null=True,
        blank=True
    )
    delivery_method = models.CharField(
        'Delivery Method',
        max_length=30,
        null=True,
        blank=True,
        choices=[
            ('Digital Download', 'Digital Download'),
            ('USPS', 'USPS'),
            ('FedEx', 'FedEx'),
            ('FedEx Customer Charged', 'FedEx Customer Charged')
        ]
    )
    fedex_customer_number = models.CharField(
        'FedEx Customer Number',
        max_length=100,
        null=True,
        blank=True
    )
    payment_method = models.CharField(
        'Payment Method',
        max_length=30,
        null=True,
        blank=True,
        choices=[
            ('Credit Card', 'Credit Card'),
            ('Check', 'Check'),
            ('Pay at Pickup', 'Pay at Pickup'),
            ('Purchase Order', 'Purchase Order')
        ]
    )
    check_number = models.CharField(
        'Check Number',
        max_length=60,
        null=True,
        blank=True
    )
    purchase_order_number = models.CharField(
        'Purchase Order Number',
        max_length=60,
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


class PosterGallerySubmission(models.Model):
    """
    Poster Gallery Submission form on tnris.org
    https://tnris.org/texas-gis-forum/<<year>>/poster-gallery
    """

    class Meta:
        db_table = 'contact_postergallery_submission'
        verbose_name = 'Poster Gallery Submission'
        verbose_name_plural = 'Poster Gallery Submissions'

    postergallery_submission_id = models.UUIDField(
        'Poster Gallery Submission ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
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
    title = models.CharField(
        'Title',
        max_length=300,
        null=True,
        blank=True
    )
    description = models.TextField(
        'Description',
        null=True,
        blank=True
    )
    phone = models.CharField(
        'Phone',
        max_length=20,
        null=True,
        blank=True
    )
    organization = models.CharField(
        'Organization',
        max_length=150,
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

    @property
    def forum_year(self):
        return self.created.strftime("%Y")

    def __str__(self):
        return self.name + " " + self.created.strftime('%Y-%m-%d %H:%M')


class TexasImageryServiceContact(models.Model):
    """
    Texas Imagery Service Contact form on tnris.org
    https://tnris.org/texas-imagery-service/
    """

    class Meta:
        db_table = 'contact_texasimageryservice'
        verbose_name = 'Texas Imagery Service Question or Comment'
        verbose_name_plural = 'Texas Imagery Service Questions or Comments'

    texasimageryservice_contact_id = models.UUIDField(
        'Texas Imagery Service Contact ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        'Name',
        max_length=150,
        null=False,
        blank=False
    )
    reason = models.CharField(
        'Reason',
        max_length=80,
        null=False,
        blank=False,
        default='Feedback/General Inquiry',
        choices=[
            ('Feedback/General Inquiry', 'Feedback/General Inquiry'),
            ('Issue Reporting', 'Issue Reporting')
        ],
        help_text="Reason for contacting"
    )
    issue_screenshot = models.URLField(
        'Issue Screenshot URL',
        max_length=255,
        null=True,
        blank=True
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
    government_agency_or_affiliation = models.CharField(
        'Government Agency or Affiliation',
        max_length=150,
        null=True,
        blank=True
    )
    question_or_comments = models.TextField(
        'Question or Comment',
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
        return self.name + " " + self.created.strftime('%Y-%m-%d %H:%M')


class TexasImageryServiceRequest(models.Model):
    """
    Texas Imagery Service Request form on tnris.org
    https://tnris.org/google-request/
    """

    class Meta:
        db_table = 'contact_texasimageryservice_request'
        verbose_name = 'Texas Imagery Service Request'
        verbose_name_plural = 'Texas Imagery Service Requests'

    texasimageryservice_request_id = models.UUIDField(
        'Texas Imagery Service Request ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    # Form fields - Submitted information
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
        max_length=35,
        null=True,
        blank=True
    )
    organization = models.CharField(
        'Organization',
        max_length=200,
        null=True,
        blank=True
    )
    contractor_access = models.CharField(
        'Contractor Access',
        max_length=3,
        default='N/A',
        choices=[
            ('N/A', 'N/A'),
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        help_text="Are you requesting access on behalf of a contractor currently under contract with your agency?"
    )
    relevant_project_of_partnership = models.CharField(
        'Relevant Project of Partnership',
        max_length=250,
        null=True,
        blank=True,
        help_text="Name of project or relevant partnership for which imagery will be used:"
    )
    company_name = models.CharField(
        'Company Name',
        max_length=150,
        null=True,
        blank=True,
        help_text="Business name of contracting company performing the work:"
    )
    name_of_qualifying_agency = models.CharField(
        'Name of Qualifying Agency',
        max_length=150,
        null=True,
        blank=True,
        help_text="Name of the qualifying agency for which you are performing work under the project or formal partnership:"
    )
    email_of_qualifying_agency = models.CharField(
        'Email of Qualifying Agency',
        max_length=150,
        null=True,
        blank=True,
        help_text="Contact email at qualifying agency with which you are formally partnering or performing contracted work:"
    )
    anticipated_project_end_date = models.CharField(
        'Anticipated Project End Date',
        max_length=150,
        null=True,
        blank=True
    )
    end_date = models.CharField(
        'End Date likely to be extended?',
        max_length=8,
        default='N/A',
        choices=[
            ('N/A', 'N/A'),
            ('No', 'No'),
            ('Possible', 'Possible'),
            ('Likely', 'Likely')
        ],
        help_text="Is the anticipated end date likely to be extended?"
    )
    best_effort = models.BooleanField(
        'Best Effort',
        default=False,
        help_text="Imagery web services are provided as a ‘best effort’ level service; there is no implied or explicit high availability service-level agreement for the imagery web services."
    )
    no_distribution = models.BooleanField(
        'No Distribution',
        default=False,
        help_text="The organization-specific web service URL or other credentials for accessing the imagery as a service may not to be distributed outside of your organization. Usage statistics will be kept to inform the acquisition of future imagery updates and to support sustained funding for the license."
    )
    horizontal_accuracy = models.BooleanField(
        'Horizontal Accuracy',
        default=False,
        help_text="Stated horizontal positional accuracy of the imagery is expected to achieve or exceed one meter (CE90) in most areas without significant vertical relief. Higher precision is expected in urban areas, where existing supplemental ground control was more abundant."
    )
    datum_transformation = models.BooleanField(
        'Datum Transformation',
        default=False,
        help_text="A datum transformation may be required to achieve the highest level of positional accuracy, especially when reprojecting imagery between NAD27, NAD83, and WGS84-based datums."
    )
    contractors = models.BooleanField(
        'Contractors',
        default=False,
        help_text="Contractors or formal partners performing work on behalf of a licensee must apply separately for access to the imagery service if it is to be used outside the immediate licensee's physical facilities or network."
    )
    reselling = models.BooleanField(
        'reselling',
        default=False,
        help_text="Imagery files may not be resold, leased, rented or redistributed outside of your immediate organization or used for projects not identified to and approved by TNRIS. Providing mass downloads of any imagery files or derivative works containing the imagery is not permitted."
    )
    primary_contact_signature = models.CharField(
        'Primary Contact Signature',
        max_length=150,
        null=True,
        blank=True
    )
    # Internal Management fields
    username = models.CharField(
        'Username',
        max_length=80,
        null=True,
        blank=True
    )
    password = models.CharField(
        'Password',
        max_length=80,
        null=True,
        blank=True
    )
    credentialed_url = models.URLField(
        'Credentialed URL',
        max_length=200,
        null=True,
        blank=True
    )
    non_credentialed_wmts_link = models.URLField(
        'Non-Credentialed WMTS Link',
        max_length=200,
        null=True,
        blank=True
    )
    non_credentialed_wms_link = models.URLField(
        'Non-Credentialed WMS Link',
        max_length=200,
        null=True,
        blank=True
    )
    notes = models.TextField(
        'Notes',
        null=True,
        blank=True
    )
    active = models.BooleanField(
        'Active?',
        default=False,
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


"""
*************************** SURVEY MODAL TEMPLATES ****************************
********* SURVEY MODALS RENDERED IN DATAHUB TO GATHER USER FEEDBACK ***********
"""

class SurveyTemplate(models.Model):
    """Display template parameters loaded into DataHub ApiModalFeed Component. Defines content and other factors of modal appearance and behavior."""

    class Meta:
        db_table = 'survey_template'
        verbose_name = 'Survey Template'
        verbose_name_plural = 'Survey Templates'

    survey_template_id = models.UUIDField(
        'Survey Template ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    survey_template_title = models.CharField(
        'Survey Name',
        null=False,
        blank=False,
        max_length=40,
        help_text='An arbitrary title or descriptor for the survey modal'
    )
    display_delay_template_type = models.PositiveSmallIntegerField(
        'Display Delay Template Type',
        null=False,
        blank=False,
        default=5,
        help_text="Integer value in seconds before modal appears."
    )
    content_type = models.CharField(
        'Display Type',
        help_text='The display type of the modal; for example, should it display a series of dialogues, or should the modal be a single, static-text alert type.',
        max_length=16,
        null=False,
        blank=False,
        default="multi-modal",
        choices=[
            ('single-modal', 'single-modal'),
            ('multi-modal', 'multi-modal')
        ],
    )
    initial_content_state = models.CharField(
        'Initial Modal Content State',
        max_length=16,
        null=False,
        blank=False,
        default='preview',
        choices=[
            ('preview', 'preview'),
            ('full', 'full'),
            ('minimized', 'minimized'),
            ('none', 'none')
        ],
        help_text="Sets the initial content of the modal upon loading. Preview content is the default initial content state."
    )
    preview_header = models.CharField(
        'Preview Modal Header',
        max_length=40,
        null=True,
        blank=True,
        help_text="The header for the Preview Content of the modal"
    )
    preview_body_text = models.CharField(
        'Preview Modal Body Text',
        max_length=400,
        null=True,
        blank=True,
        help_text="The text content for the Preview Content of the modal"
    )
    preview_accept_button_text = models.CharField(
        'Preview Modal Accept Button Text',
        max_length=20,
        null=False,
        blank=False,
        default="Accept",
        help_text="The text label for the preview accept button"
    )
    preview_reject_button_text = models.CharField(
        'Preview Modal Reject Button Text',
        max_length=20,
        null=False,
        blank=False,
        default="No Thanks",
        help_text="The text label for the preview reject button"
    )
    preview_later_button_text = models.CharField(
        'Preview Modal Later Button Text',
        max_length=20,
        null=False,
        blank=False,
        default="Maybe Later",
        help_text="The text label for the preview later button"
    )
    preview_position = models.CharField(
        'Preview Modal Position',
        max_length=16,
        null=False,
        blank=False,
        default='bottom-right',
        choices=[
            ("top-right","top-right"),
            ("top-left","top-left"),
            ("top-center","top-center"),
            ("bottom-right","bottom-right"),
            ("bottom-left","bottom-left"),
            ("bottom-center","bottom-center"),
            ("left-center","left-center"),
            ("right-center","right-center"),
            ("center","center"),
        ],
        help_text="Sets the position of the preview modal on the screen when loaded."
    )
    preview_size = models.CharField(
        'Preview Modal Size',
        max_length=14,
        null=False,
        blank=False,
        default='fit-content',
        choices=[
            ("full-screen","full-screen"), 
            ("full-height","full-height"), 
            ("full-width","full-width"),  
            ("half-width","half-width"), 
            ("half-height","half-height"),
            ("fit-content", "fit-content")
        ],
        help_text="Sets the size of the preview modal on the screen when loaded."
    )
    preview_background_color = models.CharField(
        'Preview Modal Background Overlay Color',
        max_length=32,
        null=True,
        blank=True,
        default='',
        help_text='Sets the background overlay color of the preview modal on load.'
    )
    full_header = models.CharField(
        'Full Modal Header',
        max_length=40,
        null=True,
        blank=True,
        help_text="The header for the Full Content of the modal"
    )
    full_body_text = models.TextField(
        'Full Body Text',
        null=True,
        blank=True,
        help_text="The text content for the Full Content of the modal"
    )
    full_position = models.CharField(
        'Full Modal Position',
        max_length=16,
        null=False,
        blank=False,
        default='bottom-right',
        choices=[
            ("top-right","top-right"),
            ("top-left","top-left"),
            ("top-center","top-center"),
            ("bottom-right","bottom-right"),
            ("bottom-left","bottom-left"),
            ("bottom-center","bottom-center"),
            ("left-center","left-center"),
            ("right-center","right-center"),
            ("center","center"),
        ],
        help_text="Sets the position of the preview modal on the screen when loaded."
    )
    full_size = models.CharField(
        'Full Modal Size',
        max_length=14,
        null=False,
        blank=False,
        default='full-screen',
        choices=[
            ("full-screen","full-screen"), 
            ("full-height","full-height"), 
            ("full-width","full-width"),  
            ("half-width","half-width"), 
            ("half-height","half-height"),
            ("half-screen", "half-screen"),
            ("fit-content", "fit-content")
        ],
        help_text="Sets the size of the full modal on the screen when loaded."
    )
    full_background_color = models.CharField(
        'Full Modal Background Overlay Color',
        max_length=32,
        null=True,
        blank=True,
        default='#333333c4',
        help_text='Sets the background overlay color of the full modal on load.'
    )
    minimized_icon = models.CharField(
        'MDC Icon Text String',
        max_length=40,
        null=False,
        blank=False,
        default='fact_check',
        help_text="Sets the icon for the minimized state of the modal",
    )
    minimized_text = models.CharField(
        'Minimized modal label text',
        max_length=40,
        null=False,
        blank=False,
        default='Take Survey',
        help_text="Sets the label text for the minimized state of the modal",
    )
    sheet_id = models.CharField(
        'Google Sheet Id to post responses to',
        max_length=50,
        null=True,
        blank=True,
        help_text="Sets the Google Sheet id for survey results to be posted to",
    )
    survey_id = models.CharField(
        'SurveyJS Id to pull survey from',
        max_length=50,
        null=True,
        blank=True,
        help_text="Sets the SurveyJS id for survey results to be posted to",
    )
    #===============================================================================#
    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        'Last Modified',
        auto_now=True
    )
    public = models.BooleanField(
        'Public',
        default=False
    )
    dev_mode = models.BooleanField(
        'Dev Mode',
        help_text='If checked, the modal will only display in development on localhost:3000',
        default=False
    )
    def __str__(self):
        return str(self.survey_template_id)

"""
*************************** SUBSCRIBER LISTS ****************************
********* EMAIL SUBSCRIBER LIST ENDPOINT FOR VARIED CAMPAIGNS *****************
"""
class Campaign(models.Model):
    """campaigns for email subscriptions"""
    class Meta:
        db_table = 'contact_campaign'
        verbose_name = "Campaign"
        verbose_name_plural = 'Campaigns'
        ordering = ['campaign_name']
    
    campaign_id = models.UUIDField(
        'subscription identification number',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    campaign_name = models.CharField(
        'human friendly name for campaign',
        max_length=40,
        blank=False,
        unique=True
    )
    campaign_description = models.CharField(
        'description of campaign, including limitations for use of emails, etc',
        max_length=140,
        blank=False
    )
    def __str__(self):
        return self.campaign_name

class CampaignSubscriber(models.Model):
    """Campaign subscriber model for varied email campaign subscriptions."""

    class Meta:
        db_table = 'contact_campaign_subscriber'
        verbose_name = 'Campaign Subscriber'
        verbose_name_plural = 'Campaign Subscribers'
        ordering = ['campaign__campaign_name']

    subscriber_id = models.UUIDField(
        'subscriber identification number',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE
    )
    email = models.CharField(
        'email',
        max_length=140,
        unique=True,
        blank=False,
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
        return "%s | %s" % (self.email, self.campaign)
    