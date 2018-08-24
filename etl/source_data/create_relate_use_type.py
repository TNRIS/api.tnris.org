import os
import csv
import datetime

import uuid
from dateutil import parser

def create_collection(sourcefile, fieldnames):
    outfile = 'relate-use-type.csv'

    useDict = {
        "Analysis":"750abda0-d147-4ffe-ad38-cd576395e38b",
        "Basemap":"4562297f-0362-4c49-97be-096eb2fa4107",
        "Cartography":"c912f1b2-2cbb-4af0-b222-37b4a6012649",
        "Feature Extraction":"b457ecf4-c547-4427-8e23-612ba5304082",
        "General Large Scale Geologic Information and Mapping":"3831d36e-99f2-4a9c-88b0-61dcf13d14d5",
        "Historical Use":"5e04c177-67d2-4166-81ac-d5a8ae6393d1",
        "Location":"c62158e7-6771-4b6b-a606-5bcd5d5df558",
        "Planning":"1ea95e8e-80d3-4fa0-aaea-299a29238797",
        "Research":"eb55fbd2-5848-4f54-b67c-81c5f01383dc"
    }

    with open(outfile, 'w') as outcsv:
        writer = csv.writer(outcsv)
        print(fieldnames)
        writer.writerow(i for i in fieldnames)

        with open(sourcefile) as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                ru = row['recommended_use'].strip()
                print(row['name'].strip())
                print(ru)
                for key in useDict:
                    if key in ru or key.lower() in ru:
                        newrow = [
                            uuid.uuid4(),
                            datetime.datetime.now(),
                            datetime.datetime.now(),
                            row['collection_id'].strip(),
                            useDict[key]
                        ]
                        writer.writerow(i for i in newrow)
                        print(key)

                # handle outliers
                value = ''
                if 'Historical use' in ru:
                    value = "Historical Use"
                if 'General Large scale Geologic information and mapping' in ru:
                    value = "General Large Scale Geologic Information and Mapping"
                if 'Base mapping' in ru:
                    value = "Basemap"
                if 'cartographic representation' in ru:
                    value = "Cartography"

                if value != '':
                    newrow = [
                        uuid.uuid4(),
                        datetime.datetime.now(),
                        datetime.datetime.now(),
                        row['collection_id'].strip(),
                        useDict[value]
                    ]
                    writer.writerow(i for i in newrow)
                    print(value)

if __name__ == '__main__':
    create_collection('master-processed.csv', [
        'use_relate_id',
        'created',
        'last_modified',
        'collection_id',
        'use_type_id'
        ])
