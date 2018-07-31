import os
import csv
import datetime

import uuid
from dateutil import parser

def create_collection(sourcefile, fieldnames):
    outfile = 'relate-epsg.csv'

    epsgDict = {
        '2276':"ba163cfa-61be-414b-b4b2-97fbd2a86a91",
        '2277':"a3fc3a87-78a0-43f2-ad5b-5dcf890587e3",
        '2278':"2615acb1-ad3e-4b28-a2a0-50dabc46c3b6",
        '2279':"b194d365-3e97-442e-9052-0d98d7d5d530",
        '2919':"bd7c7cb9-0299-4f9d-8503-b1b597e28c8c",
        '2964':"4e3a2703-0aea-44f2-b1f6-1031be1eb037",
        '3081':"2c46cfc7-34b3-4874-a74e-540aabc9f029",
        '3083':"a7af5118-324a-4788-b677-66c2daa0f75e",
        '3857':"4d8bd1fa-668c-4f7d-af5f-a26259675231",
        '4267':"e2e07ba9-fe5b-43e9-9dd3-721e1d324c87",
        '4269':"18cbe740-02b9-465c-b39c-5613f035ab1e",
        '4326':"4842b079-737d-40cb-86af-01437694a048",
        '6344':"649be27a-46ff-4e61-af3b-c3b1c82ec32b",
        '26913':"176945a4-aae8-480c-b8d3-f439fa4803b6",
        '26914':"b53e7baa-96a1-44ac-8ed2-e569861e3ce2",
        '26915':"d68af081-c8cb-4289-9a54-cb66b3c80d4e",
        '26916':"8facce08-0b55-4b9d-8b13-2664fac1f507",
        '32613':"b9e14716-d743-4b6e-9df8-fcff626cc643",
        '32614':"8afc240b-dcea-4e06-9dbc-a773d2fe0dcc"
    }

    with open(outfile, 'w') as outcsv:
        writer = csv.writer(outcsv)
        print(fieldnames)
        writer.writerow(i for i in fieldnames)

        with open(sourcefile) as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                if row['spatial_reference'] != '':
                    # general application of data type
                    sr_str = row['spatial_reference'].replace('<p>','').replace('</p>','').strip()
                    sr_list = sr_str.split(', ')
                    print(row['name'].strip())
                    print(sr_list)
                    for sr in sr_list:
                        code_dbl = sr.replace("<a href='https&#58;//epsg.io/",'').replace("'>EPSG ",'+').replace('</a>','')
                        if row['name'].strip() == 'FEMA 2011 1m Liberty Lidar':
                            code_dbl = code_dbl.replace("'>[EPSG ", '+')
                        # if row['name'].strip() == 'StratMap NGA\USGS 2015 1ft NC\CIR Orthoimagery':
                        #     code_dbl = code_dbl.replace("),[EPSG 32614", '')
                        code = code_dbl.split('+')[1]
                        print(code)

                        newrow = [
                            uuid.uuid4(),
                            datetime.datetime.now(),
                            datetime.datetime.now(),
                            row['collection_id'].strip(),
                            epsgDict[code]
                        ]
                        writer.writerow(i for i in newrow)


if __name__ == '__main__':
    create_collection('master-processed.csv', [
        'epsg_relate_id',
        'created',
        'last_modified',
        'collection_id',
        'epsg_type_id'
        ])
