# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .filters import (CollectionAgencyNameFilter, CollectionCountyFilter,
                      CountyDropdownFilter)

from .forms import CollectionForm, ProductForm, ImageForm, ScannedPhotoIndexLinkForm

from .models import (Agency, Collection, County, CountyRelate, FrameSize,
                     Image, LineIndex, MicroficheIndex, PhotoIndex, Product,
                     ScannedPhotoIndexLink)
from .actions import (export_collection, export_product, export_photo_index,
                      export_scanned_photo_index_link, export_county, export_line_index,
                      export_microfiche_index, export_agency_domain,
                      export_frame_size_domain, export_county_domain)
import boto3, json


class AgencyAdmin(admin.ModelAdmin):
    model = Agency
    ordering = ('name',)
    list_display = (
        'name', 'abbreviation'
    )
    actions = [export_agency_domain]


class FrameSizeAdmin(admin.ModelAdmin):
    model = FrameSize
    ordering = ('frame_size',)
    actions = [export_frame_size_domain]


class PhotoIndexInlineAdmin(admin.StackedInline):
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-closed',)
    model = PhotoIndex
    extra = 0


class ScannedPhotoIndexLinkInlineAdmin(admin.StackedInline):
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-closed',)
    model = ScannedPhotoIndexLink
    form = ScannedPhotoIndexLinkForm
    extra = 0


class LineIndexInlineAdmin(admin.StackedInline):
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-open',)
    model = LineIndex
    extra = 0


class MicroficheIndexInlineAdmin(admin.StackedInline):
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-open',)
    model = MicroficheIndex
    extra = 0


class ProductInlineAdmin(admin.StackedInline):
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-open',)
    model = Product
    form = ProductForm
    extra = 0
    ordering = ('frame_size__frame_size', 'physical_location')


class CountyRelateInlineAdmin(admin.StackedInline):
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-closed',)
    model = CountyRelate
    extra = 0
    ordering = ('county__name',)


class ImageInlineAdmin(admin.StackedInline):
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-open',)
    model = Image
    form = ImageForm
    extra = 0


class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    form = CollectionForm
    fieldsets = (
        ('Collection Information', {
             'fields': ('collection', 'agency', 'from_date', 'to_date',
                       'index_service_url', 'frames_service_url', 'mosaic_service_url',
                       'counties', 'number_of_boxes', 'photo_index_only', 'public',
                       'fully_scanned', 'thumbnail_image', 'qr_code_url'),
        }),
        ('Remarks', {
            'fields': ('remarks',)
        })
    )
    inlines = [PhotoIndexInlineAdmin, LineIndexInlineAdmin,
               MicroficheIndexInlineAdmin, ProductInlineAdmin,
               ScannedPhotoIndexLinkInlineAdmin, ImageInlineAdmin]
    list_display = (
        'collection', 'id', 'agency', 'from_date', 'to_date', 'county_names', 'public'
    )
    ordering = ('from_date', 'agency__name')
    search_fields = ('collection', 'id', 'from_date', 'to_date')
    list_filter = (
        'public',
        'fully_scanned',
        'Products__clean_status',
        CollectionAgencyNameFilter,
        CollectionCountyFilter
    )
    readonly_fields=('qr_code_url',)
    actions = [
                export_collection,
                export_product,
                export_photo_index,
                export_scanned_photo_index_link,
                export_county,
                export_line_index,
                export_microfiche_index
              ]

    def county_names(self, collection):
        county_relates = (
            CountyRelate.objects.filter(collection=collection)
                .select_related('county').values_list("county__name")
        )
        counties = sorted([c[0] for c in county_relates])
        return "{}".format(", ".join(name for name in counties))

    county_names.short_description = "Counties in Collection"

    def save_formset(self, request, form, formset, change):
        super(CollectionAdmin, self).save_formset(request, form, formset, change)
        
        if formset.model == Image:
            # fire lambda to refresh the ChcView
            # nested under if statement to ensure it only fires
            # once rather than for every inline admin
            client = boto3.client('lambda')
            payload = {'materialized_view': ['compiled_historical_collection', 'catalog_collection_meta']}
            response = client.invoke(
                FunctionName='api-tnris-org-refresh_materialized_views',
                InvocationType='Event',
                Payload=json.dumps(payload)
            )
            print(response)


class CountyAdmin(admin.ModelAdmin):
    list_filter = (
        ('name', CountyDropdownFilter),
    )
    list_per_page = 25
    ordering = ('name',)
    list_display = ('name', 'fips')
    # search_fields = ['name', 'fips']
    actions = [export_county_domain]


# Register your models here.
admin.site.register(Agency, AgencyAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(County, CountyAdmin)
admin.site.register(FrameSize, FrameSizeAdmin)
