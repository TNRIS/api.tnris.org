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
                newrow = [uuid.uuid4(), row[1], row[2], datetime.datetime.now(), datetime.datetime.now(), row[0]]
                writer.writerow(i for i in newrow)

if __name__ == '__main__':
    transformAreaCsv('data-download-area.csv', [
        'zipped_by_area_type_id',
        'zipped_by_area_type',
        'zipped_by_area_type_name',
        'created',
        'last_modified',
        'orig_data_download_id'])
