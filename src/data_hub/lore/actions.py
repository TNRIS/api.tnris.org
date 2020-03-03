from django.http import HttpResponse
import datetime, csv

from .models import (
    Collection,
    Product,
    Agency,
    County,
    FrameSize,
    PhotoIndex,
    ScannedPhotoIndexLink,
    LineIndex,
    MicroficheIndex,
    CountyRelate
)

# additional actions in admin console dropdown
# export the historical collections table from the database to .csv format
def export_collection(self, request, queryset):
    date = datetime.datetime.today().strftime('%Y%m%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_historical_collection.csv"' % date
    writer = csv.writer(response)
    # write header row
    writer.writerow([
        'collection_id',
        'collection',
        'from_date',
        'to_date',
        'agency_id',
        'photo_index_only',
        'public',
        'fully_scanned',
        'remarks',
        'created',
        'last_modified',
        'index_service_url',
        'frames_service_url',
        'mosaic_service_url',
        'ls4_link',
        'qr_code_url',
        'number_of_boxes'
    ])

    collections = queryset.values_list()

    for c in collections:
        for a in Agency.objects.filter(collection=c):
            writer.writerow([
                c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],c[10],c[11],c[12],c[13],c[14],c[15],c[16]
            ])
    return response
export_collection.short_description = "Collections table to CSV"


# export the products table from the database to .csv format
# frame sizes are based on frame size id's and relationship to frame size table
# tied to collection records; action available in CollectionAdmin class
def export_product(self, request, queryset):
    date = datetime.datetime.today().strftime('%Y%m%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_historical_product.csv"' % date
    writer = csv.writer(response)
    # writer header row
    writer.writerow([
        'collection_id',
        'product_id',
        'coverage',
        'number_of_frames',
        'medium',
        'print_type',
        'physical_location',
        'remarks',
        'created',
        'last_modified',
        'frame_size',
        'clean_status'
    ])

    collections = queryset.values_list()

    for c in collections:
        for p in Product.objects.filter(collection=c):
            for size in FrameSize.objects.filter(product=p):
                writer.writerow([
                    p.collection_id,
                    p.id,
                    p.coverage,
                    p.number_of_frames,
                    p.medium,
                    p.print_type,
                    p.physical_location,
                    p.remarks,
                    p.created,
                    p.last_modified,
                    size.frame_size,
                    p.clean_status
                ])
    return response
export_product.short_description = "Products table to CSV"


# export the photo_index table from the database to .csv format
# tied to collection records; action available in CollectionAdmin class
def export_photo_index(self, request, queryset):
    date = datetime.datetime.today().strftime('%Y%m%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_historical_photo_index.csv"' % date
    writer = csv.writer(response)
    # writer header row
    writer.writerow([
        'collection_id',
        'photo_index_id',
        'number_of_frames',
        'scanned',
        'scanned_location',
        'physical_location',
        'remarks',
        'created',
        'last_modified'
    ])

    collections = queryset.values_list()

    for c in collections:
        for photo in PhotoIndex.objects.filter(collection=c):
            writer.writerow([
                photo.collection_id,
                photo.id,
                photo.number_of_frames,
                photo.scanned,
                photo.scanned_location,
                photo.physical_location,
                photo.remarks,
                photo.created,
                photo.last_modified
            ])
    return response
export_photo_index.short_description = "Photo Index table to CSV"


# export the scanned photo index link table from the database to .csv format
# tied to collection records; action available in CollectionAdmin class
def export_scanned_photo_index_link(self, request, queryset):
    date = datetime.datetime.today().strftime('%Y%m%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_historical_scanned_photo_index_link.csv"' % date
    writer = csv.writer(response)
    # writer header row
    writer.writerow([
        'collection_id',
        'link_id',
        'year',
        'size',
        'sheet',
        'link',
        'created',
        'last_modified'
    ])

    collections = queryset.values_list()

    for c in collections:
        for link in ScannedPhotoIndexLink.objects.filter(collection=c):
            writer.writerow([
                link.collection_id,
                link.id,
                link.year,
                link.size,
                link.sheet,
                link.link,
                link.created,
                link.last_modified
            ])
    return response
export_scanned_photo_index_link.short_description = "Scanned Photo Index Link table to CSV"


# export the county table information using the county relate table
# tied to collection records; action available in CollectionAdmin class
def export_county(self, request, queryset):
    date = datetime.datetime.today().strftime('%Y%m%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_historical_county.csv"' % date
    writer = csv.writer(response)
    # writer header row
    writer.writerow([
        'collection_id',
        'county_id',
        'name',
        'fips',
        'created',
        'last_modified'
    ])

    collections = queryset.values_list()

    for c in collections:
        for r in CountyRelate.objects.filter(collection=c):
            writer.writerow([
                r.collection_id,
                r.county.id,
                r.county.name,
                r.county.fips,
                r.created,
                r.last_modified
            ])
    return response
export_county.short_description = "Counties table to CSV"


# export the line_index table information
# tied to collection records; action available in CollectionAdmin class
def export_line_index(self, request, queryset):
    date = datetime.datetime.today().strftime('%Y%m%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_historical_line_index.csv"' % date
    writer = csv.writer(response)
    # writer header row
    writer.writerow([
        'collection_id',
        'line_index_id',
        'remarks',
        'created',
        'last_modified'
    ])

    collections = queryset.values_list()

    for c in collections:
        for i in LineIndex.objects.filter(collection=c):
            writer.writerow([
                i.collection_id,
                i.id,
                i.remarks,
                i.created,
                i.last_modified
            ])
    return response
export_line_index.short_description = "Line Index table to CSV"


# export the agency domain table from the database to .csv format
# action used in AgencyAdmin
def export_agency_domain(self, request, queryset):
    date = datetime.datetime.today().strftime('%Y%m%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_historical_acquiring_agency_domain.csv"' % date
    writer = csv.writer(response)
    # write header row
    writer.writerow([
        'id',
        'name',
        'abbreviation',
        'sample_image_url',
        'media_type',
        'general_scale',
        'about',
        'created',
        'last_modified'
    ])

    agencies = queryset.values_list(
        'id',
        'name',
        'abbreviation',
        'sample_image_url',
        'media_type',
        'general_scale',
        'about',
        'created',
        'last_modified'
    )

    for a in agencies:
        writer.writerow(a)

    return response
export_agency_domain.short_description = "Acquiring Agency domain table to CSV"


# export the frame_size domain table from the database to .csv format
# action used in FrameSizeAdmin
def export_frame_size_domain(self, request, queryset):
    date = datetime.datetime.today().strftime('%Y%m%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_historical_frame_size_domain.csv"' % date
    writer = csv.writer(response)
    # write header row
    writer.writerow([
        'id',
        'frame_size',
        'created',
        'last_modified'
    ])

    frame_sizes = queryset.values_list(
        'id',
        'frame_size',
        'created',
        'last_modified'
    )

    for f in frame_sizes:
        writer.writerow(f)

    return response
export_frame_size_domain.short_description = "Frame Size domain table to CSV"


# export the county domain table from the database to .csv format
# action used in CountyAdmin
def export_county_domain(self, request, queryset):
    date = datetime.datetime.today().strftime('%Y%m%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_historical_county_domain.csv"' % date
    writer = csv.writer(response)
    # write header row
    writer.writerow([
        'id',
        'fips',
        'name',
        'created',
        'last_modified'
    ])

    counties = queryset.values_list(
        'id',
        'fips',
        'name',
        'created',
        'last_modified'
    )

    for c in counties:
        writer.writerow(c)

    return response
export_county_domain.short_description = "County domain table to CSV"
