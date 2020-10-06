from django.contrib import admin
from django.http import HttpResponse
import csv, datetime

from .models import (
    DataHubContact,
    DataHubOrder,
    DataHubOutsideEntityContact,
    EducationContact,
    EmailTemplate,
    ForumJobBoardSubmission,
    GeneralContact,
    GeorodeoCallForPresentationsSubmission,
    GeorodeoRegistration,
    LakesOfTexasContact,
    OrderMap,
    PosterGallerySubmission,
    SurveyTemplate,
    TexasImageryServiceContact,
    TexasImageryServiceRequest
)
from .filters import (
    ForumJobBoardSubmissionForumYearFilter,
    GeorodeoCallForPresentationsSubmissionYearFilter,
    GeorodeoRegistrationYearFilter,
    PosterGallerySubmissionForumYearFilter
)

# List Display Custom Action Mixins
class ExportSelectedToCsvMixin:
    def export_selected_to_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        date_str = datetime.date.today().strftime("%Y%m%d")
        model_name = self.model.__name__

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s_%s.csv' % (model_name, date_str)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_selected_to_csv.short_description = 'Export Selected to CSV'


# Register your models here.
@admin.register(DataHubContact)
class DataHubContactAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = DataHubContact
    actions = ["export_selected_to_csv"]
    list_display = (
        'name',
        'email',
        'collection',
        'uuid',
        'acquisition_date',
        'category',
        'software',
        'message',
        'created'
    )
    ordering = ('-created',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


@admin.register(DataHubOrder)
class DataHubOrderAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = DataHubOrder
    actions = ["export_selected_to_csv"]
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
class DataHubOutsideEntityContactAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = DataHubOutsideEntityContact
    actions = ["export_selected_to_csv"]
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


@admin.register(EducationContact)
class EducationContactAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = EducationContact
    actions = ["export_selected_to_csv"]
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


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    model = EmailTemplate
    list_display = (
        'email_template_type',
        'email_template_subject',
        'form_id',
        'sendpoint',
        'serializer_classname'
    )
    readonly_fields = ('email_template_id',)
    ordering = ('email_template_type',)


@admin.register(ForumJobBoardSubmission)
class ForumJobBoardSubmissionAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = ForumJobBoardSubmission
    actions = ["export_selected_to_csv"]
    list_display = (
        'name',
        'email',
        'phone',
        'organization',
        'other_notes',
        'forum_year',
        'created'
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
class GeneralContactAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = GeneralContact
    actions = ["export_selected_to_csv"]
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
class GeorodeoCallForPresentationsSubmissionAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = GeorodeoCallForPresentationsSubmission
    actions = ["export_selected_to_csv"]
    list_display = (
        'name',
        'email',
        'phone',
        'organizationtitle',
        'category',
        'title',
        'created',
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
class GeorodeoRegistrationAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = GeorodeoRegistration
    actions = ["export_selected_to_csv"]
    list_display = (
        'firstname',
        'lastname',
        'email',
        'organization',
        'vegetarian',
        'attendingsocial',
        'previouslyattended',
        'experience',
        'created',
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
class LakesOfTexasContactAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = LakesOfTexasContact
    actions = ["export_selected_to_csv"]
    list_display = (
        'name',
        'email',
        'phone',
        'industry',
        'message',
        'created'
    )
    ordering = ('-created',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


@admin.register(OrderMap)
class OrderMapAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = OrderMap
    actions = ["export_selected_to_csv"]
    list_display = (
        'type_of_data',
        'type_of_map',
        'name',
        'organization',
        'industry',
        'email',
        'phone',
        'delivery_method',
        'payment_method',
        'created'
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
class PosterGallerySubmissionAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = PosterGallerySubmission
    actions = ["export_selected_to_csv"]
    list_display = (
        'name',
        'email',
        'phone',
        'title',
        'created',
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

@admin.register(SurveyTemplate)
class SurveyTemplateAdmin(admin.ModelAdmin):
    model = SurveyTemplate
    list_display = (
        'public',
        'survey_template_title',
        'created',
        'sheet_id',
        'survey_id'
    )
    ordering = ('-created',)

@admin.register(TexasImageryServiceContact)
class TexasImageryServiceContactAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = TexasImageryServiceContact
    actions = ["export_selected_to_csv"]
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
class TexasImageryServiceRequestAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = TexasImageryServiceRequest
    actions = ["export_selected_to_csv"]
    list_display = (
        'organization',
        'active',
        'name',
        'email',
        'phone',
        'contractor_access',
        'non_credentialed_wms_link',
        'notes',
        'created'
    )
    ordering = ('-created',)
    readonly_fields = ('best_effort',
                       'no_distribution',
                       'horizontal_accuracy',
                       'datum_transformation',
                       'contractors',
                       'reselling')
    list_filter = ('active','contractor_access')
    search_fields = ('organization', 'name', 'email', 'non_credentialed_wms_link', 'notes')

    fieldsets = (
        ('Submitted Request', {
            'classes': ('grp-collapse',),
            'fields': ('name',
                    'email',
                    'phone',
                    'organization',
                    'contractor_access',
                    'relevant_project_of_partnership',
                    'company_name',
                    'name_of_qualifying_agency',
                    'email_of_qualifying_agency',
                    'anticipated_project_end_date',
                    'end_date',
                    'primary_contact_signature',
                    'best_effort',
                    'no_distribution',
                    'horizontal_accuracy',
                    'datum_transformation',
                    'contractors',
                    'reselling')
        }),
        ('Internal Management', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('username',
                    'password',
                    'credentialed_url',
                    'non_credentialed_wmts_link',
                    'non_credentialed_wms_link',
                    'notes',
                    'active')
        })
    )