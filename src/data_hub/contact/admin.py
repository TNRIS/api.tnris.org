from django.contrib import admin
from .models import (
    EmailTemplate,
    ForumJobBoardSubmission,
    GeneralContact,
    GeorodeoCallForPresentationsSubmission,
    GeorodeoRegistration,
    PosterGallerySubmission,
    TexasImageryServiceContact,
    TexasImageryServiceRequest
)
from .filters import (
    ForumJobBoardSubmissionForumYearFilter,
    GeorodeoCallForPresentationsSubmissionYearFilter,
    GeorodeoRegistrationYearFilter,
    PosterGallerySubmissionForumYearFilter
)

# Register your models here.
@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    model = EmailTemplate
    list_display = (
        'email_template_type',
        'email_template_subject',
        'email_template_id'
    )
    readonly_fields = ('email_template_id',)
    ordering = ('email_template_type',)


@admin.register(ForumJobBoardSubmission)
class ForumJobBoardSubmissionAdmin(admin.ModelAdmin):
    model = ForumJobBoardSubmission
    list_display = (
        'name',
        'email',
        'phone',
        'organization',
        'other_notes',
        'forum_year'
    )
    ordering = ('-created',)
    list_filter = (
        ForumJobBoardSubmissionForumYearFilter,
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


@admin.register(GeneralContact)
class GeneralContactAdmin(admin.ModelAdmin):
    model = GeneralContact
    list_display = (
        'name',
        'email',
        'phone',
        'address',
        'organization',
        'industry',
        'question_or_comments',
        'created'
    )
    ordering = ('-created',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


@admin.register(GeorodeoCallForPresentationsSubmission)
class GeorodeoCallForPresentationsSubmissionAdmin(admin.ModelAdmin):
    model = GeorodeoCallForPresentationsSubmission
    list_display = (
        'name',
        'email',
        'phone',
        'organizationtitle',
        'category',
        'title',
        'georodeo_year'
    )
    ordering = ('-created',)
    list_filter = (
        GeorodeoCallForPresentationsSubmissionYearFilter,
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


@admin.register(GeorodeoRegistration)
class GeorodeoRegistrationAdmin(admin.ModelAdmin):
    model = GeorodeoRegistration
    list_display = (
        'firstname',
        'lastname',
        'email',
        'organization',
        'vegetarian',
        'attendingsocial',
        'previouslyattended',
        'experience',
        'georodeo_year'
    )
    ordering = ('-created',)
    list_filter = (
        GeorodeoRegistrationYearFilter,
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


@admin.register(PosterGallerySubmission)
class PosterGallerySubmissionAdmin(admin.ModelAdmin):
    model = PosterGallerySubmission
    list_display = (
        'name',
        'email',
        'phone',
        'title',
        'forum_year'
    )
    ordering = ('-created',)
    list_filter = (
        PosterGallerySubmissionForumYearFilter,
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


@admin.register(TexasImageryServiceContact)
class TexasImageryServiceContactAdmin(admin.ModelAdmin):
    model = TexasImageryServiceContact
    list_display = (
        'name',
        'reason',
        'email',
        'phone',
        'government_agency_or_affiliation',
        'question_or_comments',
        'created'
    )
    ordering = ('-created',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


@admin.register(TexasImageryServiceRequest)
class TexasImageryServiceRequestAdmin(admin.ModelAdmin):
    model = TexasImageryServiceRequest
    list_display = (
        'name',
        'email',
        'phone',
        'organization',
        'contractor_access',
        'relevant_project_of_partnership',
        'created'
    )
    ordering = ('-created',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields