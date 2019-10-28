import os
import csv
import datetime

import uuid, psycopg2
from psycopg2.extensions import AsIs

# Database Connection Info
database = os.environ.get('DB_NAME')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')

# connection string
conn_string = "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (database, username, host, password, port)
# connect to the database
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

count = 0
readfile = "texasimageryservicerequest.csv"
with open(readfile) as infile:
    reader = csv.DictReader(infile)

    for row in reader:
        columns = row.keys()
        values = [row[column] for column in columns]
        print(values)
        bool_vals = []
        for v in values:
            va = v
            if v == 'TRUE':
                va = True
            elif v == 'FALSE':
                va = False
            else:
                va = va
            bool_vals.append(va)
        bool_vals[0] = str(uuid.uuid4())
        n = datetime.datetime.now()
        bool_vals[-1] = n
        bool_vals[-2] = n
        print(bool_vals)
        insert_statement = 'insert into contact_texasimageryservice_request (%s) values %s'

        cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(bool_vals)))
        conn.commit()
        count += 1
print(count)
cur.close()