# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .forms import MapCollectionForm
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
    inline_classes = ('grp-collapse grp-open',)
    model = MapDownload
    extra = 0

# primary
@admin.register(MapCollection)
class MapCollectionAdmin(admin.ModelAdmin):
    model = MapCollection
    form = MapCollectionForm
    fieldsets = (
        ('Map Collection/Series Information', {
             'fields': ('name', 'publish_date', 'description', 'public',
                       'thumbnail_link', 'data_collections')
        }),
    )
    inlines = [MapDownloadAdmin]
    list_display = (
        'name', 'publish_date', 'public'
    )
    ordering = ('name',)
    search_fields = ('name', 'publish_date', 'description')
    list_filter = ('public',)
