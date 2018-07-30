import os
import csv
import datetime

import uuid
from dateutil import parser

def create_collection(sourcefile, fieldnames):
    outfile = 'relate-band.csv'

    bandDict = {
    'CIR':'095105ee-1810-4697-b1f9-7d2ff3cf0e9a',
    'NC':'09f7a8d7-0ce5-4046-b22d-f6c706e3dc18',
    'BW':'9c13abc2-e472-470a-8db1-1ca6446199a3'
    }

    ohShits = [
        'National Agriculture Imagery Program (NAIP) 2008 CCM Orthoimagery',
        'City of Austin 2006 Orthoimagery',
        'National Agriculture Imagery Program (NAIP) 2009 CCM Orthoimagery',
        'NOAA 2007 Orthoimagery'
    ]

    # bandDict.keys = ['NC']

    with open(outfile, 'w') as outcsv:
        writer = csv.writer(outcsv)
        print(fieldnames)
        writer.writerow(i for i in fieldnames)

        with open(sourcefile) as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                if row['category'].strip() == 'Orthoimagery - Regional' or row['category'].strip() == 'Orthoimagery - Statewide':
                    # if 'CIR' not in row['name'].strip() and 'NC' not in row['name'].strip() and 'BW' not in row['name'].strip():
                        # print("OH SHIT", row['name'])
                    if row['name'].strip() in ohShits:
                        newrow = [
                            uuid.uuid4(),
                            datetime.datetime.now(),
                            datetime.datetime.now(),
                            bandDict['NC'],
                            row['collection_id'].strip()
                        ]
                        writer.writerow(i for i in newrow)
                    for key in bandDict.keys():
                        if key in row['name'].strip():
                            if key == 'BW' and row['name'].strip() == 'IBWC 2011 6in NC Orthoimagery':
                                continue
                            newrow = [
                                uuid.uuid4(),
                                datetime.datetime.now(),
                                datetime.datetime.now(),
                                bandDict[key],
                                row['collection_id'].strip()
                            ]
                            # print(key, row['name'])
                            writer.writerow(i for i in newrow)


if __name__ == '__main__':
    create_collection('master-processed.csv', [
        'band_relate_id',
        'created',
        'last_modified',
        'band_type_id',
        'collection_id'
        ])
