import os
import psycopg2
import datetime
import uuid
import csv

database = os.environ.get('DB_NAME')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')

conn_string = "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (database, username, host, password, port)

# connect to database
conn = psycopg2.connect(conn_string)
cur = conn.cursor()
bad = []
types = []

# open writer
with open('area_type_updated.csv', 'w') as output:
    writer = csv.writer(output)
    # insert new areas
    with open('area_type.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = 0
        for row in reader:
            if header == 0:
                writer.writerow(row)
            if header != 0:
                print(row[0])
                area_type = row[1]
                area_type_name = row[3]
                orig_data_download_id = row[4]
                area_code = row[5]
                # print(area_type, area_type_name, orig_data_download_id, area_code)

                # insert into the Database
                newUuid = uuid.uuid4()
                row[2] = newUuid
                timestamp = datetime.datetime.now()
                newQuery = "INSERT INTO area_type (area_type_id, area_type, area_type_name, orig_data_download_id, created, last_modified, area_code) VALUES ('%s', '%s', '%s', %s, '%s', '%s', '%s')" % (newUuid, area_type, area_type_name, orig_data_download_id, timestamp, timestamp, area_code)
                print(newQuery)
                try:
                    cur.execute(newQuery)
                    conn.commit()
                    writer.writerow(row)
                except Exception as e:
                    print(e)
                    conn.rollback()
                    bad.append([row[0], area_code, e])
                    if e not in types:
                        types.append(e)
            header += 1
        print(header - 1)
print("-------------------------")
print(len(bad), ' total errors')
for b in bad:
    print(b)
print("-------------------------")
for e in types:
    print(e)

###########
cur.close()
conn.close()

print("that's all folks!!")

# replicant table to rds area_type table. used for data.tnris.org maps to display county coverage, filter by geometry, and download datasets.
