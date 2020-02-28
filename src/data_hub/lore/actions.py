from django.http import HttpResponse
import datetime, csv

from .models import (
    Collection,
    Product,
    County,
    FrameSize,
    PhotoIndex,
    ScannedPhotoIndexLink,
    LineIndex,
    MicroficheIndex,
    CountyRelate,
    ChcView
)

# additional actions in admin console dropdown
# export the historical collections table from the database to .csv format
def export_collections(self, request, queryset):
    date = datetime.datetime.today().strftime('%Y%m%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_historical_collections.csv"' % date
    writer = csv.writer(response)
    # write header row
    writer.writerow([
        'collection_id',
        'collection',
        'from_date',
        'to_date',
        'public',
        'remarks',
        'created',
        'last_modified',
        'agency_id',
        'frames_service_url',
        'index_service_url',
        'ls4_link',
        'mosaic_service_url',
        'number_of_boxes',
        'qr_code_url',
        'fully_scanned',
        'photo_index_only'
    ])

    collections = queryset.values_list()

    # collections = queryset.values_list([
    #     'id',
    #     'collection',
    #     'from_date',
    #     'to_date',
    #     'public',
    #     'remarks',
    #     'created',
    #     'last_modified',
    #     'agency_id',
    #     'frames_service_url',
    #     'index_service_url',
    #     'ls4_link',
    #     'mosaic_service_url',
    #     'number_of_boxes',
    #     'qr_code_url',
    #     'fully_scanned',
    #     'photo_index_only'
    # ])

    for c in collections:
        writer.writerow([
            c.id,
            c.collection,
            c.from_date,
            c.to_date,
            c.public,
            c.remarks,
            c.created,
            c.last_modified,
            c.agency_id,
            c.frames_service_url,
            c.
        ])
    return response
export_collections.short_description = "Collections table to CSV"


# export the products table from the database to .csv format
def export_products(self, request, queryset):
    date = datetime.datetime.today().strftime('%Y%m%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_historical_products.csv"' % date
    writer = csv.writer(response)
    # writer header row
    writer.writerow([
        'collection_id',
        'coverage',
        'number_of_frames',
        'medium',
        'print_type',
        'physical_location',
        'remarks',
        'created',
        'last_modified',
        'frame_size_id',
        'clean_status'
    ])

    collections = queryset.values_list()

    for c in collections:
        for p in Product.objects.filter(collection=c):
            writer.writerow([
                p.collection_id,
                p.coverage,
                p.number_of_frames,
                p.medium,
                p.print_type,
                p.physical_location,
                p.remarks,
                p.created,
                p.last_modified,
                p.frame_size_id,
                p.clean_status
            ])
    return response
export_products.short_description = "Products table to CSV"
