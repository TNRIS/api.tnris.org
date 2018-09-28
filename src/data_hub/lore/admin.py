# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .filters import CollectionAgencyNameFilter, CollectionCountyFilter, \
    CountyDropdownFilter
from .forms import CollectionForm, ProductForm
from .models import (Agency, Collection, County, CountyRelate, FrameSize,
                     LineIndex, MicroficheIndex, PhotoIndex, Product, Scale)


class AgencyAdmin(admin.ModelAdmin):
    model = Agency
    ordering = ('name',)


class FrameSizeAdmin(admin.ModelAdmin):
    model = FrameSize
    ordering = ('frame_size',)


class ScaleAdmin(admin.ModelAdmin):
    model = Scale
    ordering = ('scale',)


class PhotoIndexInlineAdmin(admin.StackedInline):
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-closed',)
    model = PhotoIndex
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


class CountyRelateInlineAdmin(admin.StackedInline):
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-closed',)
    model = CountyRelate
    extra = 0
    ordering = ('county__name',)


class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    form = CollectionForm
    fieldsets = (
        ('Collection Information', {
             'fields': ('collection', 'agency', 'from_date', 'to_date',
                       'index_service_url', 'frames_service_url', 'mosaic_service_url',
                       'counties', 'public'),
        }),
        ('Remarks', {
            'fields': ('remarks',)
        })
    )
    inlines = [PhotoIndexInlineAdmin, LineIndexInlineAdmin,
               MicroficheIndexInlineAdmin, ProductInlineAdmin]
    list_display = (
        'collection', 'agency', 'from_date', 'to_date', 'county_names', 'public'
    )
    ordering = ('agency__name', 'from_date')
    search_fields = ('collection',)
    list_filter = (
        'public',
        CollectionAgencyNameFilter,
        CollectionCountyFilter
    )

    def county_names(self, collection):
        county_relates = (
            CountyRelate.objects.filter(collection=collection)
                .select_related('county').values_list("county__name")
        )
        counties = sorted([c[0] for c in county_relates])
        return "{}".format(", ".join(name for name in counties))

    county_names.short_description = "Counties in Collection"


# Register your models here.
class CountyAdmin(admin.ModelAdmin):
    list_filter = (
        ('name', CountyDropdownFilter),
    )
    list_per_page = 25
    ordering = ('name',)
    list_display = ('name', 'fips')
    # search_fields = ['name', 'fips']


admin.site.register(Agency, AgencyAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(County, CountyAdmin)
admin.site.register(FrameSize, FrameSizeAdmin)
admin.site.register(Scale, ScaleAdmin)
