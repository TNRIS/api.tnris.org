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

# insert degree blocks
with open('deg_blocks.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = 0
    for row in reader:
        if header != 0:
            area_code = row[3]
            area_type_name = row[2].title() + '|' + row[1]
            print(area_code, area_type_name)

            # insert into the Database
            newUuid = uuid.uuid4()
            timestamp = datetime.datetime.now()
            newQuery = "INSERT INTO area_type (area_type_id, area_type, area_type_name, orig_data_download_id, created, last_modified, area_code) VALUES ('%s', '%s', '%s', %s, '%s', '%s', '%s')" % (newUuid, 'block', area_type_name, 666666, timestamp, timestamp, area_code)
            print(newQuery)
            # cur.execute(newQuery)
            # conn.commit()
        header += 1
    print(header - 1)

# insert 250k
with open('deg_250k.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = 0
    for row in reader:
        if header != 0:
            area_code = row[2]
            area_type_name = row[1]
            print(area_code, area_type_name)

            # insert into the Database
            newUuid = uuid.uuid4()
            timestamp = datetime.datetime.now()
            newQuery = "INSERT INTO area_type (area_type_id, area_type, area_type_name, orig_data_download_id, created, last_modified, area_code) VALUES ('%s', '%s', '%s', %s, '%s', '%s', '%s')" % (newUuid, '250k', area_type_name, 666666, timestamp, timestamp, area_code)
            print(newQuery)
            # cur.execute(newQuery)
            # conn.commit()
        header += 1
    print(header - 1)

###########
cur.close()
conn.close()

print("that's all folks!!")
