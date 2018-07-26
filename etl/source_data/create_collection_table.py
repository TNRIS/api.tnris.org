import os
import csv
import datetime

import uuid

def create_collection(sourcefile, fieldnames):
    outfile = 'collection.csv'
    with open(outfile, 'w') as outcsv:
        writer = csv.writer(outcsv)
        print(fieldnames)
        writer.writerow(i for i in fieldnames)

        with open(sourcefile) as infile:
            reader = csv.DictReader(infile)

            for row in reader:

                # print(datetime.datetime.now())
                newrow = [row['collection_id'],
                    row['name'],
                    row['date_added'],
                    row['short_description'],
                    row['description'],
                    ,
                    ,
                    row['known_issues'],
                    row['filename'],
                    row['wms_link'],
                    row['pop_link'],
                    row['status_map_cartodb_id'],
                    row['overview_image_url'],
                    row['thumb_url'],
                    row['natural_image_url'],
                    row['urban_image_url'],
                    row['tile_index'],
                    row['supplemental_report_url'],
                    row['lidar_breaklines_url'],
                    row['coverage_extent'],
                    row['tags'],
                    datetime.datetime.now(),
                    datetime.datetime.now(),
                    row['license'],
                    ,

                ]
                # newrow = [row[], row[0], row[2], row[0], datetime.datetime.now(), datetime.datetime.now()]
                # writer.writerow(i for i in newrow)

if __name__ == '__main__':
    create_collection('master-processed.csv', [
        'collection_id',
        'name',
        'acquisition_date',
        'short_description',
        'description',
        'authoritative',
        'public',
        'known_issues',
        'md_filename',
        'wms_link',
        'popup_link',
        'carto_map_id',
        'overview_image',
        'thumbnail_image',
        'natural_image',
        'urban_image',
        'tile_index_url',
        'supplemental_report_url',
        'lidar_breaklines_url',
        'coverage_extent',
        'tags',
        'created',
        'last_modified',
        'license',
        'source',
        'license_type_id',
        'source_type_id',
        'template_type_id'
        ])
