from django.contrib import admin
from .models import (
    DataHubContact,
    DataHubOrder,
    DataHubOutsideEntityContact,
    EmailTemplate,
    ForumJobBoardSubmission,
    GeneralContact,
    GeorodeoCallForPresentationsSubmission,
    GeorodeoRegistration,
    LakesOfTexasContact,
    OrderMap,
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
@admin.register(DataHubContact)
class DataHubContactAdmin(admin.ModelAdmin):
    model = DataHubContact
    list_display = (
        'name',
        'email',
        'collection',
        'uuid',
        'category',
        'software',
        'message'
    )
    ordering = ('-created',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


@admin.register(DataHubOrder)
class DataHubOrderAdmin(admin.ModelAdmin):
    model = DataHubOrder
    list_display = (
        'name',
        'email',
        'phone',
        'address',
        'organization',
        'industry',
        'harddrive',
        'delivery',
        'payment',
        'created'
    )
    ordering = ('-created',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


@admin.register(DataHubOutsideEntityContact)
class DataHubOutsideEntityContactAdmin(admin.ModelAdmin):
    model = DataHubOutsideEntityContact
    list_display = (
        'name',
        'email',
        'category',
        'software',
        'send_to_email',
        'send_to_name',
        'message',
        'created'
    )
    ordering = ('-created',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


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


@admin.register(LakesOfTexasContact)
class LakesOfTexasContactAdmin(admin.ModelAdmin):
    model = LakesOfTexasContact
    list_display = (
        'name',
        'email',
        'phone',
        'industry',
        'message'
    )
    ordering = ('-created',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


@admin.register(OrderMap)
class LakesOfTexasContactAdmin(admin.ModelAdmin):
    model = OrderMap
    list_display = (
        'type_of_data',
        'type_of_map',
        'name',
        'organization',
        'industry',
        'email',
        'phone',
        'delivery_method',
        'payment_method'
    )
    ordering = ('-created',)
    fieldsets = (
        ('General Info', {
            'classes': ('grp-collapse',),
            'fields': ('name',
                       'address_1',
                       'address_2',
                       'city',
                       'state',
                       'zip',
                       'email',
                       'phone',
                       'fax',
                       'organization',
                       'industry',
                       'industry_other',
                       'delivery_method',
                       'fedex_customer_number',
                       'payment_method',
                       'check_number',
                       'purchase_order_number',
                       'type_of_data',
                       'type_of_map',
                       'additional_info')
        }),
        ('Federal Prints', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('map_option',
                       'map_description')
        }),
        ('Pre-Made Maps', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('map_collection_name',
                       'map_sheet',
                       'legislative_request')
        }),
        ('Custom Maps', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('map_size',
                       'custom_map_size',
                       'map_scale',
                       'map_title',
                       'map_date')
        })
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