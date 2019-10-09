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
        blank=False,
        help_text="Layman text/name of Form Submission table/model class."
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
        'General Contact ID',
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
        default='No',
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
        default="N/A",
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
        max_length=150,
        null=True,
        blank=True
    )
    contractor_access = models.CharField(
        'Contractor Access',
        max_length=3,
        null=True,
        blank=True,
        default='No',
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        help_text="Are you requesting access on behalf of a contractor currently under contract with your agency?"
    )
    relevant_project_of_partnership = models.CharField(
        'Relevant Project of Partnership',
        max_length=150,
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
        null=True,
        blank=True,
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
