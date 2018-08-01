import os
import csv
import datetime

import uuid
from dateutil import parser

def create_collection(sourcefile, fieldnames):
    outfile = 'relate-resolution.csv'

    resolutionDict = {
        "10m":"62ca721b-d639-44ff-9761-bbc4183727ee",
        "120cm":"347be2de-0c01-4469-8bf2-ea8f22a5b384",
        "140cm":"81bb3337-3052-4f5f-a84b-ff1098f90d41",
        "150cm":"e806744f-f1d7-4c98-9907-e008589c091b",
        "1ft":"90857264-f804-46c8-89ee-ebdda95332cc",
        "1m":"528227f2-e1e1-4018-99f8-4ae62821436d",
        "2m":"60eda1d7-83ed-4833-9478-6520d8423bb3",
        "30cm":"5685ab92-079f-4ea9-85a2-c2844cfb51e7",
        "30m":"12b72fc3-6c89-43a3-8e94-772b676be9bc",
        "35cm":"dbcc5ab0-019c-4df3-b301-90eb149d8ebc",
        "3in":"52fe48c1-446c-49df-a8a6-7d38890938d0",
        "50cm":"1407c25b-40ec-4488-864f-d3c675b96282",
        "60cm":"a8ad536b-b8bc-42de-8ba1-155ab538aa32",
        "61cm":"47bc11f3-fc93-4671-8df1-fe0c9aeef738",
        "6in":"856b8002-9da7-4d93-836f-97e14ec1f9ae",
        "70cm":"2f882368-218d-49d5-b307-52407f055e85",
        "9in":"6450f6ce-95ec-4042-95a2-8a9c3fa41ede"
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
