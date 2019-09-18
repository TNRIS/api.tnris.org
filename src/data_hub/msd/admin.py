# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .forms import MapCollectionForm, MapDownloadForm
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
@admin.register(MapDownload)
class MapDownloadAdmin(admin.ModelAdmin):
    model = MapDownload
    form = MapDownloadForm
    ordering = ('map_collection_id', 'label')
    list_display = (
        'map_collection_id', 'label', 'map_size', 'pixels_per_inch'
    )
    list_filter = (
        'map_collection_id', 'label', 'map_size', 'pixels_per_inch'
    )

    # remove default action 'delete_selected' so s3 files will be deleted by the
    # model's overridden delete method. also so user permissions don't have to be
    # handled.
    def get_actions(self, request):
        actions = super(MapDownloadAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


# primary
@admin.register(MapCollection)
class MapCollectionAdmin(admin.ModelAdmin):
    model = MapCollection
    form = MapCollectionForm
    fields = (
        'name',
        'publish_date',
        'description',
        'public',
        'thumbnail_link',
        'delete_thumbnail',
        'data_collections'
    )
    list_display = (
        'name', 'publish_date', 'public'
    )
    ordering = ('name',)
    search_fields = ('name', 'publish_date', 'description')
    list_filter = ('public',)

    # remove default action 'delete_selected' so s3 files will be deleted by the
    # model's overridden delete method. also so user permissions don't have to be
    # handled.
    def get_actions(self, request):
        actions = super(MapCollectionAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
