import os
import csv
import datetime

import uuid
from dateutil import parser

def create_relate(sourcefile, fieldnames):
    outfile = 'relate-category.csv'

    categoryDict = {
        'Boundary':'379edcc0-5867-41bd-b383-075baa830d59',
        'Reference Grid':'4c0b549c-9409-4093-80a9-ae166a899645',
        'Demographics':'5d1b4f08-a934-46bf-9d6c-05ef9dba4f68',
        'Transportation':'5dbbdf04-8f63-4cec-b1f5-00bf00ac9f19',
        'Hydrography':'6695100b-dfe0-4e0d-9f63-f4bff3c6fd93',
        'Geology':'7b5b09a2-4de1-4774-8f9d-382fcd9eae82',
        'Land Use - Land Cover':'965d75a1-a4f1-40e4-ab93-725a5700d7c5',
        'Floodplain':'9aa3b308-c419-4597-b455-a08c929d3225',
        'Topographic Map':'9ad48d76-6d9a-4df0-8455-313e7eee1385',
        'Bathymetry':'a12c269c-da39-4fb7-ac0e-cb8c21f345b7',
        'Cultural':'a5ba4241-894d-4e77-9fcc-9c3d89a93892',
        'Orthoimagery':'a77f0e4b-1703-4c7c-a8ea-b0ab73f6b0cf',
        'Lidar':'ac9bdad4-39ec-48e8-9de4-35b96dbccf08',
        'Historic Imagery':'b4b0411f-5dcb-47ba-b16a-ac90a44b5f36',
        'Weather':'e059472d-4e36-4013-95f3-dd10b8a92d42',
        'Environmental':'e10bd935-4122-4a9b-89c2-333a0039759e',
        'Natural Regions':'e3f23c9f-b2ef-4956-aba7-b1af77a7dd39',
        'Elevation':'e5b98127-64f0-4e21-8a19-2d279dfc134a'
        }

    with open(outfile, 'w') as outcsv:
        writer = csv.writer(outcsv)
        print(fieldnames)
        writer.writerow(i for i in fieldnames)

        with open(sourcefile) as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                if row['category'].strip() == 'Orthoimagery - Regional' or row['category'].strip() == 'Orthoimagery - Statewide':
                    # print(categoryDict['Orthoimagery'])
                    newrow = [
                        uuid.uuid4(),
                        datetime.datetime.now(),
                        datetime.datetime.now(),
                        categoryDict['Orthoimagery'],
                        row['collection_id'].strip()
                    ]
                    writer.writerow(i for i in newrow)
                else:
                    # print(row['category'])
                    newrow = [
                        uuid.uuid4(),
                        datetime.datetime.now(),
                        datetime.datetime.now(),
                        categoryDict[key],
                        row['collection_id'].strip()
                    ]
                    writer.writerow(i for i in newrow)


if __name__ == '__main__':
    create_relate('master-processed.csv', [
        'category_relate_id',
        'created',
        'last_modified',
        'category_type_id',
        'collection_id'
        ])
