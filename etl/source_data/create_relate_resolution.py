import os
import csv
import datetime

import uuid
from dateutil import parser

def create_collection(sourcefile, fieldnames):
    outfile = 'relate-resolution.csv'

    resolutionDict = {
        "10m":"90a2f0a9-3a27-4595-8949-59d9855452d4",
        "120cm":"5b7317d7-7e09-41bd-95c6-635dc2f92d68",
        "140cm":"3a07d07c-b0ca-4fbb-9661-89a0cdb585e2",
        "150cm":"3a9a2b04-4a59-4e4f-93ec-9e4779a07ef7",
        "1ft":"90857264-f804-46c8-89ee-ebdda95332cc",
        "1m":"528227f2-e1e1-4018-99f8-4ae62821436d",
        "2m":"178bbb0e-64a4-46b3-98f3-0e9e02b861f4",
        "30cm":"acfdbff6-7968-4d00-9858-0e6f1ae9c2ac",
        "30m":"12b72fc3-6c89-43a3-8e94-772b676be9bc",
        "35cm":"dbcc5ab0-019c-4df3-b301-90eb149d8ebc",
        "3in":"52fe48c1-446c-49df-a8a6-7d38890938d0",
        "50cm":"1407c25b-40ec-4488-864f-d3c675b96282",
        "60cm":"ec4d219d-adad-4521-9b6a-ef7b9e9d0c56",
        "61cm":"024c0334-d841-4558-8bc7-4c921936bb2b",
        "6in":"856b8002-9da7-4d93-836f-97e14ec1f9ae",
        "70cm":"f687a773-c56c-4763-a4e1-6bca28d28f09",
        "9in":"a5b24325-c37e-4b3b-bb50-806711435736"
    }

    with open(outfile, 'w') as outcsv:
        writer = csv.writer(outcsv)
        print(fieldnames)
        writer.writerow(i for i in fieldnames)

        with open(sourcefile) as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                title = row['title'].strip()
                print(title)
                # general application of present resolutions
                for key in resolutionDict:
                    if key in title:
                        if key == '50cm' and '150cm' in title:
                            continue
                        newrow = [
                            uuid.uuid4(),
                            datetime.datetime.now(),
                            datetime.datetime.now(),
                            row['collection_id'].strip(),
                            resolutionDict[key]
                        ]
                        writer.writerow(i for i in newrow)
                        print(key)

                # handle outliers
                value = ''
                if "70 cm" in title:
                    value = "70cm"
                if "50 cm" in title:
                    value = "50cm"
                if "12in" in title:
                    value = "1ft"
                if "1M" in title:
                    value = "1m"
                if title == 'City of Austin 2006':
                    value = "6in"

                if value != '':
                    newrow = [
                        uuid.uuid4(),
                        datetime.datetime.now(),
                        datetime.datetime.now(),
                        row['collection_id'].strip(),
                        resolutionDict[value]
                    ]
                    writer.writerow(i for i in newrow)
                    print(value)

if __name__ == '__main__':
    create_collection('master-processed.csv', [
        'resolution_relate_id',
        'created',
        'last_modified',
        'collection_id',
        'resolution_type_id'
        ])
