# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (MapCollection,
                     MapDataRelate,
                     MapDownload,
                     MapSize,
                     PixelsPerInch)


# domains
@admin.register(MapSize)
class MapSizeAdmin(admin.ModelAdmin):
    model = MapSize
    ordering = ('label',)
    list_display = (
        'label', 'length', 'width'
    )

@admin.register(PixelsPerInch)
class PixelsPerInchAdmin(admin.ModelAdmin):
    model = PixelsPerInch
    ordering = ('pixels_per_inch',)
    list_display = (
        'pixels_per_inch',
    )


# inlines

class MapDownloadAdmin(admin.StackedInline):
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-closed',)
    model = MapDownload
    extra = 0

# primary
@admin.register(MapCollection)
class MapCollectionAdmin(admin.ModelAdmin):
    model = MapCollection
    # form = CollectionForm
    fieldsets = (
        ('Map Collection/Series Information', {
             'fields': ('name', 'publish_date', 'description', 'public',
                       'thumbnail_link')
        }),
    )
    inlines = [MapDownloadAdmin]
    list_display = (
        'name', 'publish_date', 'public'
    )
    ordering = ('name',)
    search_fields = ('name', 'publish_date', 'description')
    list_filter = ('public',)

    # def county_names(self, collection):
    #     county_relates = (
    #         CountyRelate.objects.filter(collection=collection)
    #             .select_related('county').values_list("county__name")
    #     )
    #     counties = sorted([c[0] for c in county_relates])
    #     return "{}".format(", ".join(name for name in counties))
    #
    # county_names.short_description = "Counties in Collection"
