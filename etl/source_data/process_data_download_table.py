import os
import csv
import datetime

import uuid

def transformAreaCsv(sourcefile, fieldnames):
    outfile = os.path.splitext(sourcefile)[0] + '-processed.csv'
    with open(outfile, 'w') as outcsv:
        writer = csv.writer(outcsv)
        print(fieldnames)
        writer.writerow(i for i in fieldnames)

        with open(sourcefile) as infile:
            reader = csv.reader(infile)
            for row in reader:
                print(datetime.datetime.now())
                newrow = [uuid.uuid4(), row[1], row[2], row[0], datetime.datetime.now(), datetime.datetime.now()]
                writer.writerow(i for i in newrow)

if __name__ == '__main__':
    transformAreaCsv('data-download-area.csv', [
        'area_type_id',
        'area_type',
        'area_type_name',
        'orig_data_download_id',
        'created',
        'last_modified'
        ])
