import os
import csv
import datetime

import uuid
from dateutil import parser

def create_relate(sourcefile, fieldnames):
    outfile = 'relate-filetype.csv'

    ftypeDict = {
        'GDB':'08a67ef8-cbea-4b6f-a4ad-e58334290fbe',
        'ESRI GRID':'15a8d9a4-dd27-44fb-ac3f-16606eeb37f5',
        'SID':'17a5dcba-ff5e-4e81-8d3b-694096a125e9',
        'LAS':'3f961385-f5cf-400f-b04b-2cb58bce4908',
        'DEM':'45457c8c-a705-4dcc-a4a5-e84ebe980ad0',
        'MrSID':'4d67196a-da90-457d-a8f5-973ba2d37e73',
        'SHP':'5fef469d-da26-4279-b2e9-094721af176c',
        'TIFF':'60503dfb-e5a8-4017-8f78-757fb3d68ff6',
        'ECW':'67651c42-fadc-49c5-aa5a-ea62566c8974',
        'DWG':'6d00823e-bf76-4892-96a1-91cefdde5ffe',
        'JP2':'70124f34-80be-4774-8ffe-3ff966e09ac9',
        'JPG':'75f52f41-82c4-41ad-8ab4-617a72745440',
        'PDF':'aa6fadda-afc7-4963-b0d1-f0c71c470e34',
        'IMG':'aab2ded2-843d-4852-b2d7-5d2979b2e085',
        'KMZ':'ee5de03c-07cd-4af3-8cff-d9685f79491b',
        'KML':'f4adc6bc-7314-4848-87de-ced1361db873',
        '':''
        }

    oddBalls = {
        'Shapefile':ftypeDict['SHP'],
        'Shapefiles':ftypeDict['SHP'],
        'JPEG 2000':ftypeDict['JP2'],
        "JPEG2000":ftypeDict['JP2'],
        'Jp2':ftypeDict['JP2'],
        'Mr. Sid':ftypeDict['MrSID'],
        'GeoTIFF':ftypeDict['TIFF'],
        'GeoTiff':ftypeDict['TIFF'],
        'Geo-TIFF':ftypeDict['TIFF'],
        'Tiff':ftypeDict['TIFF'],
        'Geodatabase':ftypeDict['GDB'],
        'Geo-Database':ftypeDict['GDB'],
        'File Geodatabase':ftypeDict['GDB'],
        'FGDB':ftypeDict['GDB'],
        'PGDB':ftypeDict['GDB'],
        'GRID':ftypeDict['ESRI GRID'],
    }

    with open(outfile, 'w') as outcsv:
        writer = csv.writer(outcsv)
        print(fieldnames)
        writer.writerow(i for i in fieldnames)

        with open(sourcefile) as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                # handle formats with mutliple values separated by commas
                if ',' in row['available_formats'].strip():
                    ftypes = row['available_formats'].split(',')
                    for f in ftypes:
                        if f.strip() not in ftypeDict.keys():
                            print("multiples special case - using oddBalls dict: ", f.strip())
                            newrow = [
                                uuid.uuid4(),
                                datetime.datetime.now(),
                                datetime.datetime.now(),
                                row['collection_id'].strip(),
                                oddBalls[f.strip()]
                            ]
                            writer.writerow(i for i in newrow)
                        else:
                            print("multiples special case - using ftype dict: ", f.strip())
                            newrow = [
                                uuid.uuid4(),
                                datetime.datetime.now(),
                                datetime.datetime.now(),
                                row['collection_id'].strip(),
                                ftypeDict[f.strip()]
                            ]
                            writer.writerow(i for i in newrow)

                # handle non multiple values that match oddBalls dict keys
                elif row['available_formats'].strip() in oddBalls.keys():
                    print("non multiples - using oddBalls dict: ", row['available_formats'].strip())
                    f = row['available_formats'].strip()
                    print(oddBalls[f])
                    newrow = [
                        uuid.uuid4(),
                        datetime.datetime.now(),
                        datetime.datetime.now(),
                        row['collection_id'].strip(),
                        oddBalls[f]
                    ]
                    writer.writerow(i for i in newrow)

                # handle non multiple values that match ftype dict keys
                elif row['available_formats'].strip() in ftypeDict.keys():
                    print("value good by default - using ftype dict: ", row['available_formats'].strip())
                    f = row['available_formats'].strip()
                    print(ftypeDict[f])
                    newrow = [
                        uuid.uuid4(),
                        datetime.datetime.now(),
                        datetime.datetime.now(),
                        row['collection_id'].strip(),
                        ftypeDict[f]
                    ]
                    writer.writerow(i for i in newrow)

                # these are the special special cases - weird values/characters
                elif row['available_formats'].strip() == "Shapefile and Raster":
                    print("LEFTOVER!!!!!!!: ", row['available_formats'].strip())
                    newrow = [
                        uuid.uuid4(),
                        datetime.datetime.now(),
                        datetime.datetime.now(),
                        row['collection_id'].strip(),
                        ftypeDict['SHP']
                    ]
                    writer.writerow(i for i in newrow)

                elif row['available_formats'].strip() == "TIFF. JP2":
                    print("LEFTOVER!!!!!: ", row['available_formats'].strip())
                    ftypes = row['available_formats'].split('.')
                    print(ftypes)
                    for f in ftypes:
                        x = f.strip()
                        newrow = [
                            uuid.uuid4(),
                            datetime.datetime.now(),
                            datetime.datetime.now(),
                            row['collection_id'].strip(),
                            ftypeDict[x]
                        ]
                        writer.writerow(i for i in newrow)


if __name__ == '__main__':
    create_relate('master-processed.csv', [
        'file_type_relate_id',
        'created',
        'last_modified',
        'collection_id',
        'file_type_id'
        ])
