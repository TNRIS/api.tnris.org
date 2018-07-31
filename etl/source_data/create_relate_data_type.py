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

                # handle exceptions to general applciation
                # if row['name'].strip() == 'Coastal Impact Assistance Program':
                #     value = 'Raster'
                #     v.remove(row['name'])
                #     r.append(row['name'])
                #     print('CIAP handled')

                newrow = [
                    uuid.uuid4(),
                    datetime.datetime.now(),
                    datetime.datetime.now(),
                    row['collection_id'].strip(),
                    dataDict[value]
                ]
                # print(key, row['name'])
                writer.writerow(i for i in newrow)

    print(len(l), len(r), len(v))


if __name__ == '__main__':
    create_collection('master-processed.csv', [
        'data_type_relate_id',
        'created',
        'last_modified',
        'collection_id',
        'data_type_id'
        ])
