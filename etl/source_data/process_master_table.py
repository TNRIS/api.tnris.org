import os
import csv
import datetime

import uuid

def transform_master_csv(sourcefile):
    outfile = os.path.splitext(sourcefile)[0] + '-processed.csv'
    with open(outfile, 'w') as outcsv:
        writer = csv.writer(outcsv)
        # print(fieldnames)
        # writer.writerow(i for i in fieldnames)

        with open(sourcefile) as infile:
            reader = csv.reader(infile)
            counter = 0
            for row in reader:
                if counter == 0:
                    row.append('collection_id')
                    print(row)
                    writer.writerow(i for i in row)
                else:
                    row.append(uuid.uuid4())
                    print(row)
                    writer.writerow(i for i in row)
                counter += 1

if __name__ == '__main__':
    transform_master_csv('master.csv')
