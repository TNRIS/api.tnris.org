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
def export_csv(self, request, queryset):
    date = datetime.datetime.today().strftime('%Y%m%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_compiled_historical_collection.csv"' % date
    writer = csv.writer(response)
    writer.writerow([
        'collection_id',
        'collection',
        'from_date',
        'to_date',
        'agency',
        'photo_index_only',
        'public',
        'fully_scanned',
        'collection_remarks',
        'collection_created',
        'collection_last_modified',
        'index_service_url',
        'frames_service_url',
        'mosaic_service_url',
        'ls4_link',
        'qr_code_url',
        'number_of_boxes',
        'frame_size',
        'number_of_frames',
        'medium',
        'print_type'
    ])
    collections = queryset.values_list()
    # print(collections)
    for c in collections:
        for p in Product.objects.filter(collection=c):
            product_relates = (
                p.values_list(
                    'frame_size', 'coverage', 'number_of_frames', 'medium', 'print_type', 'clean_status', 'physical_location', 'product_remarks'
                )
        )
        county_relates = (
            CountyRelate.objects.filter(collection=c)
                .select_related('county').values_list("county__name")
        )
        # photo_index = PhotoIndex.objects.filter(collection=c)
        # products = sorted([p[0] for p in product_relates])
        print(product_relates)
        counties = sorted([c[0] for c in county_relates])
        print(counties)
        # print("{}".format(", ".join(name for name in counties)))
        # frame_size = FrameSize.objects.filter(collection=c)
        # microfiche = MicroficheIndex.objects.filter(collection=c)
        # line_index = LineIndex.objects.filter(collection=c)
        # link = ScannedPhotoIndexLink.objects.filter(collection=c)
        # print(c)
        # writer.writerow([
        #     c.id,
        #     c.collection,
        #     c.from_date,
        #     c.to_date,
        #     c.agency,
        #     c.photo_index_only,
        #     c.public,
        #     c.fully_scanned,
        #     c.remarks,
        #     c.created,
        #     c.last_modified,
        #     c.index_service_url,
        #     c.frames_service_url,
        #     c.mosaic_service_url,
        #     c.ls4_link,
        #     c.qr_code_url,
        #     c.number_of_boxes,
        #     product.frame_size,
        #     product.number_of_frames,
        #     product.medium,
        #     product.print_type
        # ])

    return response
export_csv.short_description = "Export Selected Records to CSV"
