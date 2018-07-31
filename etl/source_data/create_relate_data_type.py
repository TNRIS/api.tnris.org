import os
import csv
import datetime

import uuid
from dateutil import parser

def create_collection(sourcefile, fieldnames):
    outfile = 'relate-data-type.csv'

    dataDict = {
        'Lidar':"729fc18f-89bd-4df8-80e2-5b8bab949b38",
        'Vector':"79ac875b-06d6-41bb-805c-60031cb8472f",
        'Raster':"7b4f9522-8080-422b-912e-a1d289a20dbe"
    }

    one_off_rasters = ['National Elevation Dataset (NED) 2013',
                       'National Elevation Dataset (NED) 2011',
                       'Shuttle Radar Topography Mission',
                       'National Elevation Dataset (NED) Hillshade',
                       'Federal Emergency Management Agency D FIRM',
                       'Geologic Atlas of Texas',
                       'National Wetlands Inventory 062k',
                       'National Wetlands Inventory 024k',
                       'National Wetlands Inventory 100K',
                       'National Land Cover Database 2006',
                       'National Land Cover Database 2001',
                       'National Land Cover Database 2011',
                       'National Land Cover Database 1992']

    raster_and_vector = ['Bathymetry TX Coast v0.1', 'TPWD Texas Ecological Systems Data']

    l = []
    v = []
    r = []

    with open(outfile, 'w') as outcsv:
        writer = csv.writer(outcsv)
        print(fieldnames)
        writer.writerow(i for i in fieldnames)

        with open(sourcefile) as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                # general application of data type
                if row['category'].strip() == 'Lidar':
                    value = 'Lidar'
                    l.append(row['name'])
                elif (row['category'].strip() == 'Orthoimagery - Regional' or
                     row['category'].strip() == 'Orthoimagery - Statewide' or
                     row['category'].strip() == 'Topographic Map' or
                     row['category'].strip() == 'Historic Imagery'):
                    value = 'Raster'
                    r.append(row['name'])
                else:
                    value = 'Vector'
                    v.append(row['name'])

                # handle one off exceptions
                if row['name'].strip() in one_off_rasters:
                    value = 'Raster'
                    v.remove(row['name'])
                    r.append(row['name'])
                    print('%s handled' % row['name'].strip())

                newrow = [
                    uuid.uuid4(),
                    datetime.datetime.now(),
                    datetime.datetime.now(),
                    row['collection_id'].strip(),
                    dataDict[value]
                ]
                writer.writerow(i for i in newrow)

                # handle raster and vectors
                if row['name'].strip() in raster_and_vector:
                    newrow = [
                        uuid.uuid4(),
                        datetime.datetime.now(),
                        datetime.datetime.now(),
                        row['collection_id'].strip(),
                        dataDict['Raster']
                    ]
                    writer.writerow(i for i in newrow)
                    r.append(row['name'])
                    print('%s also a raster' % row['name'].strip())

    print(len(l), len(r), len(v), len(raster_and_vector))


if __name__ == '__main__':
    create_collection('master-processed.csv', [
        'data_type_relate_id',
        'created',
        'last_modified',
        'collection_id',
        'data_type_id'
        ])
