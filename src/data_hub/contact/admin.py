from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from django_json_widget.widgets import JSONEditorWidget
from django import forms
from django.shortcuts import redirect

import csv, datetime, json, os, secrets, hashlib, time
from .new_contacts import resend_email

from .models import (
    Campaign,
    CampaignSubscriber,
    DataHubContact,
    DataHubOrder,
    OrderType,
    OrderDetailsType,
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

@admin.register(OrderType)
class OrderTypeAdmin(admin.ModelAdmin): 
    model = OrderType
    actions = ["resend_order_link_email"]
    list_filter = (['order_approved', 'order_sent', 'archived'])
    list_display = (
        'id',
        'link_to_details',
        'approved_charge',
        'order_approved',
        'customer_notified',
        'order_sent',
        'archived',
        'created',
        'last_modified'
    )
    list_editable = (['approved_charge', 'customer_notified', 'order_approved', 'order_sent', 'archived'])
    list_per_page = 10
    ordering = ('-created',)

    def link_to_details(self, obj):
        link=reverse("admin:contact_orderdetailstype_change", args=[obj.order_details.id])
        return format_html(u'<a href="%s">Details</a>' % (link))
    link_to_details.allow_tags=True

    @admin.action(
        description="Resend a link to the payment portal."
    )
    def resend_order_link_email(self, request, queryset):
        resend_email(self, request, queryset, False)

    @admin.action(
        description="Resend a link to the payment portal. And CC stratmap. For troubleshooting."
    )
    def resend_order_link_email_with_cc(self, request, queryset):
        resend_email(self, request, queryset, True)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields

@admin.register(OrderDetailsType)
class OrderDetailsTypeAdmin(admin.ModelAdmin):

    def name_field(self, obj):
        if "name" in json.loads(obj.details):
            return json.loads(obj.details)["name"]
        else:
            return ""

    def email_field(self, obj):
        if "email" in json.loads(obj.details):
            return json.loads(obj.details)["email"]
        else:
            return ""

    def phone_field(self, obj):
        if "phone" in json.loads(obj.details):
            return json.loads(obj.details)["phone"]
        else:
            return ""

    def address_field(self, obj):
        obj_details = json.loads(obj.details)
        if "address" in obj_details:    
            return obj_details["address"]
        elif "address_1" in obj_details and "address_2" in obj_details:
            return obj_details["address_1"] + " " + obj_details["address_2"]
        else:
            return ""

    def organization_field(self, obj):
        if "organization" in json.loads(obj.details):
            return json.loads(obj.details)["organization"]
        else:
            return ""

    def city_field(self, obj):
        if "city" in json.loads(obj.details):
            return json.loads(obj.details)["city"]
        else:
            return ""

    def state_field(self, obj):
        if "state" in json.loads(obj.details):
            return json.loads(obj.details)["state"]
        else:
            return ""

    def zipcode_field(self, obj):
        if "zipcode" in json.loads(obj.details):
            return json.loads(obj.details)["zipcode"]
        elif "zip" in json.loads(obj.details):
            return json.loads(obj.details)["zip"]
        else:
            return ""

    def industry_field(self, obj):
        obj_details = json.loads(obj.details)
        if "industry" in obj_details:
            if "industry_other" in obj_details:
                return obj_details["industry"] + " " + obj_details["industry_other"]
            else:
                return obj_details["industry"]
        else:
            return ""

    def notes_field(self, obj):
        obj_details = json.loads(obj.details)
        if "notes" in obj_details:
            return obj_details["notes"]
        elif "additional Info" in obj_details:
            return obj_details["additional Info"]
        else:
            return ""

    def fedex_field(self, obj):
        obj_details = json.loads(obj.details)
        if "fedex" in obj_details:
            return obj_details["fedex"]
        elif "fedex customer number" in obj_details:
            return obj_details["fedex customer number"]
        else:
            return ""

    def delivery_field(self, obj):
        obj_details = json.loads(obj.details)
        if "delivery" in obj_details:
            return obj_details["delivery"]
        elif "delivery method" in obj_details:
            return obj_details["delivery method"]
        else:
            return ""

    def harddrive_field(self, obj):
        if "harddrive" in json.loads(obj.details):
            return json.loads(obj.details)["harddrive"]
        else:
            return ""

    def payment_field(self, obj):
        obj_details = json.loads(obj.details)
        if "payment" in obj_details:
            return obj_details["payment"]
        elif "payment method" in obj_details:
            return obj_details["payment method"]
        else:
            return ""

    def order_field(self, obj):
        obj_details = json.loads(obj.details)
        if "order" in obj_details:
            return obj_details["order"]
        elif "form_id" in obj_details and obj_details["form_id"] == "order-map":
            details = ""
            if "type of data" in obj_details:
                details += "type of data: " + obj_details["type of data"]
            
            if "type of map" in obj_details: 
                details += "\n type of map: " + obj_details["type of map"]

            if "map size" in obj_details: 
                details += "\n map size: " + obj_details["map size"]
            
            if "custom map size" in obj_details: 
                details += "\n custom map size: " + obj_details["custom map size"]

            if "map scale" in obj_details:
                details += "\n map scale: " + obj_details["map scale"]

            if "map title" in obj_details:
                details += "\n map title: " + obj_details["map title"]

            if "map date" in obj_details:
                details += "\n map date: " + obj_details["map date"]

            if "map collection name" in obj_details:
                details += "\n map collection name: " + obj_details["map collection name"]

            if "map sheet" in obj_details:
                details += "\n map sheet: " + obj_details["map sheet"]
            
            if "legislative request?" in obj_details:
                details += "\n legislative request?: " + obj_details["legislative request?"]

            if "map option" in obj_details:
                details += "\n map option: " + obj_details["map option"]

            if "map description" in obj_details:
                details += "\n map description: " + obj_details["map description"]

            return details
        else:
            return ""

    order_field.widget=forms.CharField(widget=JSONEditorWidget)

    def formid_field(self, obj):
        if "form_id" in json.loads(obj.details):
            return json.loads(obj.details)["form_id"]
        else:
            return ""

    def get_readonly_fields(self, request, obj=None):
        return ['id', 'name_field', 'email_field', 'phone_field', 'address_field', 'city_field', 'state_field', 'zipcode_field', 'organization_field', 'industry_field', 'fedex_field', 'notes_field', 'delivery_field', 'harddrive_field',
        'payment_field', 'order_field', 'formid_field']

    list_display = (
        [ 'id' ]
    )
    def save_model(self, request, obj, form, change):
        if(change and form.cleaned_data["update_email"] and len(form.cleaned_data["update_email"])):
            obj_details = json.loads(obj.details)
            obj_details["Email"] = form.cleaned_data["update_email"]
            setattr(obj, "details", json.dumps(obj_details))
            #setattr(form.cleaned_data, 'update_email', '')
            form.cleaned_data["update_email"] = ""
            obj.update_email = ""
            access_token = obj_details["Email"] 
            salt = secrets.token_urlsafe(32)
            pepper = os.environ.get("ACCESS_PEPPER")
            hash = hashlib.sha256(bytes(access_token + salt + pepper, 'utf8')).hexdigest()
            otp = secrets.token_urlsafe(12)

            obj.access_salt = salt
            obj.access_code = hash
            obj.otp = hashlib.sha256(bytes(otp + salt + pepper, 'utf8')).hexdigest()
            obj.otp_age=time.time()

        super().save_model(request, obj, form, change)
    def response_change(self, request, obj):
        return redirect('/admin/contact/orderdetailstype/' + str(obj.id) + '/change/')
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
        'survey_template_title',
        'public',
        'last_modified',
        'created',
        'sheet_id',
        'survey_id'
    )
    ordering = ('-last_modified',)

    fieldsets = (
        (None, {
            'fields': ('survey_template_title',
                       'sheet_id',
                       'survey_id',
                       'public',
                       'dev_mode',
                       'content_type',
                       'display_delay_template_type',
                       'initial_content_state',
                       ),
        }),
        ('Preview Modal', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('preview_header',
                       'preview_body_text',
                       'preview_accept_button_text',
                       'preview_reject_button_text',
                       'preview_later_button_text',
                       'preview_position',
                       'preview_size',
                       'preview_background_color',
                       ),
        }),
        ('Full / Survey Modal', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('full_header',
                       'full_body_text',
                       'full_position',
                       'full_size',
                       'full_background_color',
                       ),
        }),
        ('Minimized Modal', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('minimized_text',
                       'minimized_icon',
                       ),
        })
    )

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

@admin.register(CampaignSubscriber)
class CampaignSubscriberAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = CampaignSubscriber
    actions = ["export_selected_to_csv"]
    list_display = (
        'subscriber_id',
        'campaign',
        'email',
        'created',
        'last_modified'
    )
    ordering = ('campaign', 'created', 'email', 'last_modified')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin, ExportSelectedToCsvMixin):
    model = CampaignSubscriber
    actions = ["export_selected_to_csv"]
    list_display = (
        'campaign_id',
        'campaign_name',
        'campaign_description'
    )
    ordering = ('campaign_name',)
