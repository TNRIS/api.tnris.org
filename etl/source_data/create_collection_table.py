import os
import csv
import datetime

import uuid
from dateutil import parser

def create_collection(sourcefile, fieldnames):
    outfile = 'collection.csv'
    agency_dict = {
        "Capital Area Council of Governments":"26a5ae1c-42b4-4e97-8226-613856d5c3ab",
        "Federal Emergency Management Agency":"d3bcda14-d484-4628-924b-d66c778ec254",
        "FEMA":"d3bcda14-d484-4628-924b-d66c778ec254",
        "Houston-Galveston Area Council":"5b84701f-4768-4c71-9688-fef3b85047df",
        "International Boundary and Water Commission":"8cf5c57e-082a-4601-bdf3-ab415e27b5b0",
        "Lower Colorado River Authority":"87cb93e0-ed61-4ba3-a392-93b203e4d6a8",
        "North Central Texas Council of Governments":"a98b70a1-204b-46a3-9a13-65884c86e5a4",
        "Texas Commission on Environmental Quality":"a91ede8b-e37e-43ad-9457-c4f1230c5b9a",
        "Texas Department of Transportation":"d5c20a43-5b51-4c4a-8b48-629a2b87c3ee",
        "Texas General Land Office":"855f3cdc-e25d-4470-8e0d-8be483414792",
        "Texas Natural Resources Information System":"520d75b3-a503-48df-ae8d-da9775fb84bf",
        "Texas Parks and Wildlife Department":"70817c70-7364-45a8-971a-00908a95a111",
        "Texas Water Development Board":"c1e7ed1a-8bfa-44eb-980d-788bf66bed41",
        "United States Department of Agriculture":"77e1eb26-96d8-4415-bf70-a29d7f679ca9",
        "United States Fish and Wildlife Service":"68e6407d-3839-4a77-8428-6913888c168a",
        "United States Geological Survey":"2ebfd5dc-152b-4332-82ac-a6570a0f1a4c",
        "":""
    }
    license_dict = {
        "CC0":"593a35c8-9527-4e32-a3bf-c59c56173dd9",
        "NA":""
    }
    with open(outfile, 'w') as outcsv:
        writer = csv.writer(outcsv)
        print(fieldnames)
        writer.writerow(i for i in fieldnames)

        with open(sourcefile) as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                print(license_dict[row['license'].strip()])
                newrow = [
                    row['collection_id'].strip(),
                    row['name'].strip(),
                    row['date_added'].strip(),
                    row['short_description'].strip(),
                    row['description'].strip(),
                    row['source'].strip(),
                    True,
                    True,
                    row['known_issues'].strip(),
                    row['filename'].strip(),
                    row['wms_link'].strip(),
                    row['pop_link'].strip(),
                    row['status_map_cartodb_id'].strip(),
                    row['overview_image_url'].strip(),
                    row['thumb_url'].strip(),
                    row['natural_image_url'].strip(),
                    row['urban_image_url'].strip(),
                    row['tile_index_url'].strip(),
                    row['supplemental_report_url'].strip(),
                    row['lidar_breaklines_url'].strip(),
                    row['coverage_extent'].strip(),
                    row['tags'].strip(),
                    datetime.datetime.now(),
                    datetime.datetime.now(),
                    agency_dict[row['agency'].strip()],
                    license_dict[row['license'].strip()],
                    '40d5e189-a34c-40f3-aa24-632bf1fab596'
                ]
                # newrow = [row[], row[0], row[2], row[0], datetime.datetime.now(), datetime.datetime.now()]
                writer.writerow(i for i in newrow)


if __name__ == '__main__':
    create_collection('master-processed.csv', [
        'collection_id',
        'name',
        'acquisition_date',
        'short_description',
        'description',
        'source',
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
        'agency_type_id',
        'license_type_id',
        'template_type_id'
        ])
